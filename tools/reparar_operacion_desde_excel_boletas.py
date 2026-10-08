import argparse
import os
import sys

from psycopg2.extras import execute_values

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import database
from routers.base_operaciones_camiones import (
    combinar_fecha_hora_excel,
    corregir_rango_lecturas_excel,
    dividir_empresa_producto,
    excel_get,
    leer_filas_excel_base_operaciones,
    normalizar_fecha,
    normalizar_guia_excel,
    sincronizar_cuotas_cant_retiro,
    valor_excel_invalido_texto,
)


def filas_normalizadas(path_excel):
    headers, filas_excel = leer_filas_excel_base_operaciones(path_excel)
    rows = []
    for fila in filas_excel:
        if not fila:
            continue
        row_dict = dict(zip(headers, fila))
        guia = excel_get(row_dict, "guia")
        if guia is None or str(guia).strip() == "":
            continue
        empresa = excel_get(row_dict, "empresa")
        producto = excel_get(row_dict, "producto")
        empresa_producto = excel_get(row_dict, "empresa_producto")
        empresa_split, producto_split = dividir_empresa_producto(empresa_producto)
        if empresa_split and valor_excel_invalido_texto(empresa):
            empresa = empresa_split
        if producto_split and valor_excel_invalido_texto(producto):
            producto = producto_split
        buque = excel_get(row_dict, "buque")
        fecha = excel_get(row_dict, "fecha", "fecha_ingreso")
        fecha_ingreso = excel_get(row_dict, "fecha_ingreso", "fecha")
        fecha_salida = excel_get(row_dict, "fecha_salida")
        hora_ingreso = excel_get(row_dict, "hora_ingreso")
        hora_salida = excel_get(row_dict, "hora_salida")
        bodega_numero = excel_get(row_dict, "bodega_numero")
        peso_vacio = excel_get(row_dict, "peso_vacio")
        peso_lleno = excel_get(row_dict, "peso_lleno")
        lectura_ingreso = combinar_fecha_hora_excel(fecha_ingreso, hora_ingreso)
        lectura_salida = combinar_fecha_hora_excel(fecha_salida or fecha_ingreso, hora_salida)
        lectura_ingreso, lectura_salida = corregir_rango_lecturas_excel(lectura_ingreso, lectura_salida)
        rows.append(
            (
                normalizar_guia_excel(guia, buque),
                str(empresa).strip() if empresa is not None else None,
                str(producto).strip() if producto is not None else None,
                normalizar_fecha(fecha),
                int(float(bodega_numero)) if bodega_numero not in (None, "") else None,
                float(peso_vacio) if peso_vacio not in (None, "") else None,
                float(peso_lleno) if peso_lleno not in (None, "") else None,
                lectura_ingreso,
                lectura_salida,
            )
        )
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--operacion-id", type=int, required=True)
    parser.add_argument("--excel", required=True)
    parser.add_argument("--limpiar-cierre-oficial", action="store_true")
    args = parser.parse_args()

    rows = filas_normalizadas(args.excel)
    if not rows:
        raise SystemExit("No encontre filas de boletas en el Excel.")

    conn = database.get_connection()
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            rows_update = [(*row, args.operacion_id) for row in rows]
            execute_values(
                cur,
                """
                UPDATE public.base_operaciones_camiones AS b
                SET empresa = data.empresa,
                    producto = data.producto,
                    fecha = data.fecha,
                    bodega_numero = data.bodega_numero,
                    peso_vacio = data.peso_vacio,
                    peso_lleno = data.peso_lleno,
                    lectura_ingreso = data.lectura_ingreso,
                    lectura_salida = data.lectura_salida
                FROM (VALUES %s) AS data(
                    guia, empresa, producto, fecha, bodega_numero, peso_vacio,
                    peso_lleno, lectura_ingreso, lectura_salida, operacion_id
                )
                WHERE b.operacion_id = data.operacion_id
                  AND b.guia = data.guia;
                """,
                rows_update,
                template="(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                page_size=1000,
                fetch=False,
            )
            cuotas = sincronizar_cuotas_cant_retiro(cur, args.excel, args.operacion_id)
            if args.limpiar_cierre_oficial:
                for table in (
                    "operaciones_buque_cierre_bodega",
                    "operaciones_buque_cierre_cliente",
                    "operaciones_buque_cierre_tiempo",
                ):
                    cur.execute(
                        """
                        DO $$
                        BEGIN
                            IF to_regclass(%s) IS NOT NULL THEN
                                EXECUTE format('DELETE FROM public.%I WHERE operacion_id = $1', %s)
                                USING %s;
                            END IF;
                        END $$;
                        """,
                        (f"public.{table}", table, args.operacion_id),
                    )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print(f"Boletas reparadas desde Excel: {len(rows)} fila(s). Cuotas sincronizadas: {cuotas}.")


if __name__ == "__main__":
    main()
