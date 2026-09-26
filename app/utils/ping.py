import os
from dotenv import load_dotenv
from app.core.config import settings
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

def ping_s3_bucket(bucket_name: str) -> bool:
    """
    Simula um 'ping' no Amazon S3 testando a conexão e acesso ao bucket especificado.
    :return: True se a conexão/permissões estiverem OK, False caso contrário.
    """

    s3_client = boto3.client('s3')
    
    try:
        # Tenta checar a existência e permissão do bucket
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ Conexão com o S3 OK! Bucket '{bucket_name}' acessível.")
        return True

    except NoCredentialsError:
        print("❌ Erro de Credenciais: AWS Access Key ou Secret Key não foram encontradas.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"❌ Erro 404: O bucket '{bucket_name}' não existe.")
        elif error_code == '403':
            print(f"❌ Erro 403: Acesso negado ao bucket '{bucket_name}'. Verifique suas chaves/permissões.")
        else:
            print(f"❌ Erro na AWS S3 ({error_code}): {e}")
    except Exception as e:
        print(f"❌ Erro inesperado ao conectar ao S3: {e}")

    return False

# Teste local
if __name__ == "__main__":
    ping_s3_bucket("tcc-terraform")