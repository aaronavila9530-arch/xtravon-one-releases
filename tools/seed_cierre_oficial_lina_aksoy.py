import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import database
from routers.reportes_buque import DDL_CIERRE_OFICIAL_REPORTES


BODEGAS = [
    (1, "BODEGA 1", "MAIZ", 11175.614, 11073.520, 99.09, 381, 102.094, 0.91, 3.51, 70.00, 158.19, 0.65),
    (2, "BODEGA 2", "MAIZ", 13164.039, 13174.790, 100.08, 462, -10.751, -0.08, -0.38, 59.50, 221.43, -0.05),
    (3, "BODEGA 3", "MAIZ", 2667.736, 2794.480, 104.75, 94, -126.744, -4.75, -4.26, 11.33, 246.64, -0.51),
    (4, "BODEGA 4B", "SOYA", 12428.236, 12430.830, 100.02, 373, -2.594, -0.02, -0.08, 64.66, 192.25, -0.01),
    (5, "BODEGA 5", "MAIZ", 10991.708, 10950.200, 99.62, 384, 41.508, 0.38, 1.46, 67.66, 161.84, 0.26),
]


CLIENTES = [
    ("MAIZ", "DOS PINOS", 1, "DETALLE", 38.601, 14668.076, 525.81, 14673.310, 100.036, 526.00, 27.896, -5.234, -0.19),
    ("MAIZ", "TERNERINA", 2, "DETALLE", 5.192, 1972.732, 65.63, 1983.880, 100.565, 66.00, 30.059, -11.148, -0.37),
    ("MAIZ", "AGROPECUARIA EL SURCO", 3, "DETALLE", 56.215, 21361.321, 729.87, 21335.800, 99.881, 729.00, 29.267, 25.521, 0.87),
    ("MAIZ", "TOTAL MAIZ:", 10, "RESUMEN", 100.008, 37999.097, 1321.19, 37992.990, 99.984, 1321.00, 28.761, 6.107, 0.31),
    ("MAIZ", "TOTAL MAIZ", 11, "RESUMEN", 75.354, 37999.097, 1321.19, 37992.990, 99.984, 1321.00, 28.761, 6.107, 0.31),
    ("MAIZ", "INOLASA", 12, "RESUMEN", 24.646, 12428.236, 372.92, 12430.830, 100.021, 373.00, 33.327, -2.594, -0.08),
    ("MAIZ", "TOTAL EMBARQUE:", 13, "RESUMEN", 100.000, 50427.333, 1694.11, 50423.820, 99.993, 1694.00, 29.766, 3.513, 0.24),
]


def main():
    database.sql(DDL_CIERRE_OFICIAL_REPORTES)
    row = database.sql(
        """
        SELECT id
        FROM public.operaciones_buque
        WHERE UPPER(nombre_buque) IN ('MV LINA AKSOY', 'M/V LINA AKSOY')
        ORDER BY fecha_inicio ASC, id ASC
        LIMIT 1;
        """,
        fetchone=True,
    )
    if not row:
        raise SystemExit("No encontre la operacion MV LINA AKSOY.")
    operacion_id = row[0]

    database.sql("DELETE FROM public.operaciones_buque_cierre_bodega WHERE operacion_id = %s;", (operacion_id,))
    database.sql("DELETE FROM public.operaciones_buque_cierre_cliente WHERE operacion_id = %s;", (operacion_id,))
    database.sql("DELETE FROM public.operaciones_buque_cierre_tiempo WHERE operacion_id = %s;", (operacion_id,))

    for item in BODEGAS:
        database.sql(
            """
            INSERT INTO public.operaciones_buque_cierre_bodega (
                operacion_id, orden, etiqueta, producto, cantidad_bl, retirado_tm, retirado_pct,
                retirado_viajes, saldo_tm, saldo_pct, saldo_viajes, horas_trabajadas,
                rendimiento, saldo_horas
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (operacion_id, *item),
        )

    for item in CLIENTES:
        database.sql(
            """
            INSERT INTO public.operaciones_buque_cierre_cliente (
                operacion_id, producto, empresa, orden, grupo, cuota_pct, cuota_tm, cuota_viajes,
                retirado_tm, retirado_pct, retirado_viajes, promedio_x_viaje, pendiente_tm,
                pendiente_viajes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (operacion_id, *item),
        )

    database.sql(
        """
        INSERT INTO public.operaciones_buque_cierre_tiempo (
            operacion_id, producto, horas_trabajadas, tiempo_contratado, tiempo_transcurrido,
            tiempo_disponible, pct_tiempo_transcurrido, fecha_texto, hora_texto
        )
        VALUES (%s, 'MAIZ', 86.10, 151.16, 318.54, -167.38, 211.00, '6-Jul-26', '6:00 p. m.');
        """,
        (operacion_id,),
    )
    print(f"Cierre oficial cargado para MV LINA AKSOY operacion_id={operacion_id}.")


if __name__ == "__main__":
    main()
