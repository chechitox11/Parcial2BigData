import boto3
import logging
from botocore.exceptions import ClientError
import time
import statistics

precio_historial = []

def process_records(records):
    global precio_historial
    for record in records:

        data = record['Data']
        # Decodificar el dato de la secuencia como una cadena
        data_str = data.decode('utf-8')
        # Convertir la cadena en un diccionario
        data_dict = eval(data_str)
        # Obtener el precio de la acción
        precio = data_dict['close']
        
        precio_historial.append(precio)  # Agregar precio al historial
        
        
        if len(precio_historial) >= 21:
            # Realizar el cálculo de la franja inferior de Bollinger y definir un umbral
            
            print(precio_historial[:-1])
            print(len(precio_historial[:-1]))
            precio_historial_ = precio_historial[:-1]
            bollingerSuperior = bollingerSup(precio_historial_)
            print("Precio",precio)
            print("Bollinger",bollingerSuperior)
            print("\n\n")
            
            if precio > bollingerSuperior:
                # Si el precio está por debajo de la franja inferior, generar una alerta
                generarAlerta(precio, bollingerSuperior)
            
            # Limitar el historial a los últimos 20 precios
            precio_historial = precio_historial[-20:]

def bollingerSup(precio):
    bollinger = None

    if isinstance(precio, list) and len(precio) >= 20:
        mediaMovil = sum(precio[-20:]) / len(precio[-20:])
        stdMovil = statistics.stdev(precio[-20:])
        bollinger = mediaMovil + (2 * stdMovil)

    return bollinger

def generarAlerta(precio, bollingerSuperior):
    # Lógica para generar una alerta cuando el precio está por debajo de la franja inferior
    print(f"Alerta: el precio está por encima de la franja superior de Bollinger ({bollingerSuperior})")
    print("Precio actual:", precio)


def main():
    stream_name = 'kinesisbig'
    
    try:
        kinesis_client = boto3.client('kinesis')

        response = kinesis_client.describe_stream(StreamName=stream_name)
        shard_id = response['StreamDescription']['Shards'][3]['ShardId']

        response = kinesis_client.get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'
        )
        
        shard_iterator = response['ShardIterator']
        max_records = 100
        record_count = 0

        while record_count < max_records:
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=1
            )
            
            shard_iterator = response['NextShardIterator']
            records = response['Records']
            record_count += len(records)
            process_records(records)
            try:
                print(records[0]["Data"])
            except:
             pass
            
    except ClientError as e:
        logger = logging.getLogger()
        logger.exception("Couldn't get records from stream %s.", stream_name)
        raise


if __name__ == "__main__":
    main()
