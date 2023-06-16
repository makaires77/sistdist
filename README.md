# Resiliência e disponibilidade
Exercícios em Sistemas Distribuídos

## Arquivo de configuração do Docker Compose 
`docker-compose.yml`
- `version: '3'`: Isso define a versão do formato do arquivo Docker Compose que está sendo usado. No caso do seu exemplo, a versão 3 está sendo usada.
- `services`: Esta é a seção principal onde você define os serviços que serão executados em contêineres.
- `nginx`: Esta seção define o serviço Nginx. As configurações para esse serviço incluem:
  - `image: nginx:1.19.0`: Especifica a imagem do Nginx e sua versão a ser usada para criar o contêiner.
  - `ports: - 8080:80`: Mapeia a porta 8080 do host para a porta 80 do contêiner, permitindo acessar o Nginx no host através da porta 8080.
  - `volumes: - ./nginx.conf:/etc/nginx/nginx.conf:ro`: Monta o arquivo `nginx.conf` localizado no diretório atual (`./`) no caminho `/etc/nginx/nginx.conf` dentro do contêiner. O modificador `ro` significa que o volume é apenas leitura.
  - `depends_on: - wordpress1 - wordpress2 - wordpress3`: Especifica que o serviço Nginx depende dos serviços `wordpress1`, `wordpress2` e `wordpress3` para que o Docker Compose inicie esses serviços antes de iniciar o Nginx.
  
- `mysql`: Esta seção define o serviço MySQL. As configurações para esse serviço incluem:
  - `image: mysql:5.7`: Especifica a imagem do MySQL e sua versão a ser usada para criar o contêiner.
  - `environment: MYSQL_ROOT_PASSWORD: r00t`: Define a variável de ambiente `MYSQL_ROOT_PASSWORD` com o valor `r00t`, que define a senha do usuário root do MySQL.
  - `volumes: - db_data:/var/lib/mysql`: Cria um volume chamado `db_data` e o monta no caminho `/var/lib/mysql` dentro do contêiner MySQL. Isso permite que os dados do MySQL sejam persistidos mesmo que o contêiner seja reiniciado ou substituído.
  
- `wordpress1`, `wordpress2`, `wordpress3`: Essas seções definem os serviços WordPress. As configurações para cada serviço são semelhantes, mas com algumas alterações para garantir a separação e escalabilidade das instâncias do WordPress. As configurações incluem:
  - `image: wordpress:5.4.2-php7.2-apache`: Especifica a imagem do WordPress e sua versão a ser usada para criar o contêiner.
  - `depends_on: - mysql`: Especifica que o serviço WordPress depende do serviço MySQL para que o Docker Compose inicie o MySQL antes de iniciar o WordPress.
  - `environment`: Define variáveis de ambiente relacionadas à configuração do WordPress, como o host, usuário, senha e nome do banco de dados.
  - `volumes: - wordpress:/var/www/html`: Cria um volume chamado `wordpress` e o monta no caminho `/var/www/html` dentro do contêiner do WordPress. Isso permite que os dados e arquivos do WordPress sejam persistidos mesmo que o contêiner seja reiniciado ou substituído.

  
- `volumes`: Esta seção define os volumes que serão usados pelos serviços. Neste exemplo, temos dois volumes: `db_data` e `wordpress`. Esses volumes permitem que os dados persistam além da vida do contêiner.

Essa configuração do Docker Compose permite executar o Nginx como um balanceador de carga para as instâncias do WordPress. 
O Nginx é acessível na porta 8080 do host, e as instâncias do WordPress se comunicam com o serviço MySQL para armazenar e recuperar dados.

## Configuração do Nginx
`nginx.conf`
events {
  worker_connections  1024;
}

http {
  upstream wordpress {
    server wordpress1:80;
    server wordpress2:80;
    server wordpress3:80;
  }

  server {
    listen 80;

    location / {
      proxy_pass http://wordpress;
    }
  }
}
