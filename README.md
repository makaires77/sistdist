# Resiliência e disponibilidade
Exercícios em Sistemas Distribuídos

Proponha um teste usando locust que permita identificar o ponto ótimo para a mudança de uma arquitetura de soluções para sistemas computacionais em arquitetura monolítica para arquitetura de microsserviços usando como parâmetro de otimização duas variáveis: armazenamento em cache vesus latência de requisições

## Teste automatizado de carga e instâncias
O código `teste_carga.ps1' é um script em PowerShell que executa um teste de escalabilidade e desempenho de um aplicativo WordPress usando a ferramenta Locust.

Funcionamento passo a passo:

O código inicia um loop foreach para percorrer cada usuário na lista $usersList.
Dentro desse primeiro loop, há um segundo loop foreach que percorre cada instância na lista $instancesList.
Antes de iniciar o teste com um determinado número de usuários e instâncias, ele exibe uma mensagem usando o comando Write-Host, informando quantas instâncias estão sendo usadas e quantos usuários serão simulados.

Em seguida, é executado o comando docker-compose up -d para iniciar as instâncias do WordPress usando o Docker Compose. O número de instâncias é definido usando a opção --scale para escalar o serviço "wordpress1", "wordpress2" e "wordpress3" para o número especificado.

O código aguarda 30 segundos usando o comando Start-Sleep para dar tempo suficiente para que as instâncias do WordPress sejam inicializadas corretamente.

Depois disso, há um terceiro loop foreach que itera de 1 até o número de instâncias atualmente em teste ($i).
Dentro desse terceiro loop, é feito um teste de conectividade para cada instância do WordPress. O código tenta fazer uma solicitação HTTP para a URL da instância e, se a solicitação for bem-sucedida, exibe uma mensagem informando que o teste de conectividade passou. Caso contrário, exibe uma mensagem informando que o teste de conectividade falhou.

Após o teste de conectividade, o código exibe uma mensagem informando que o teste com o número de usuários e instâncias atual está sendo executado usando o Locust.

O comando locust é executado com vários parâmetros, como -f locustfile.py para especificar o arquivo de configuração do Locust, -u $u para definir o número de usuários simulados, -r 10 para definir a taxa de geração de usuários, --run-time $testDuration para definir a duração do teste e --host=$targetHost para especificar o host de destino.

O resultado do teste é salvo em um arquivo CSV usando a opção --csv=output_u_${u}_i_${i}. O nome do arquivo CSV inclui o número de usuários ($u) e o número de instâncias ($i) para identificação.

Por fim, o comando docker-compose down é executado para desligar e remover as instâncias do WordPress.
O script executa esse conjunto de ações para cada combinação de usuários e instâncias fornecidas nas listas $usersList e $instancesList.

Esse código é útil para automatizar o teste de escalabilidade e desempenho de um aplicativo WordPress usando o Locust, permitindo a simulação de diferentes cargas de usuários e números de instâncias.

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


# Trabalhos futuros associados:
## Custo-benefício para adotar microsserviços em momentos estratégicos

# Registro de entrevista com especialistas:
Luke Blaney é engenheiro-chefe do Financial Times. Alexandra Noonan é engenheira de software na Segment. Manuel Pais é um consultor e formador organizacional de TI independente, focado em interações de equipas, práticas de entrega e fluxo acelerado. Matt Heath é engenheiro da Monzo.

Um conselho para o público sobre adoção ou amadurecimento de sua arquitetura de microsserviços? 

Certifique-se de estar extremamente familiarizado com os trade-offs e de ter uma boa história sobre cada um deles, e de estar confortável com esses trade-offs ao fazer a troca.

Microsserviços são realmente benéficos se estiverem alinhados com o fluxo de valor do negócio. Isso acontece o tempo todo, basta entrar no Twitter e você verá pessoas reclamando: "Eu tenho microsserviços, mas para qualquer tipo de recurso ou mudança de negócios, preciso ter coordenação entre três, quatro ou cinco equipes de microsserviços diferentes." Não era isso que você queria alcançar em primeiro lugar, essa capacidade de implantação independente. Além disso, "fluxos de negócios independentes são o objetivo". Não é apenas o lado técnico por si só.

Blaney: Eu acho que muito disso é sobre manter o controle do que você tem. Ele pode facilmente fugir de você. Você começa com alguns e pensa: "Estes são fáceis", mas tendo que vincular dados, monitorar todas essas coisas, acompanhar tudo. Faça isso desde o início. Não espere até que você tenha 100 microsserviços e então pergunte: "Qual foi o primeiro que construímos?" Comece pelo início. Certifique-se de documentar essas coisas à medida que avança. Porque uma vez que você tem muitos deles, é muito fácil perder um na mistura.

Pais: Primeiro, comece a avaliar a carga cognitiva de sua equipe. Esse é um problema comum. Felizmente, temos propriedade de ponta a ponta nas equipes, mas sejam quais forem suas responsabilidades, certifique-se de que o tamanho do software e outras responsabilidades correspondam à sua capacidade cognitiva. Existe uma definição específica do que é carga cognitiva, mas você pode procurá-la. Essencialmente, pergunte às equipes, porque também há um aspecto psicológico aqui, se as pessoas não entenderem bem sua parte do sistema, sejam microsserviços ou outra coisa. Se eles se sentirem ansiosos, se eu tiver que ficar de plantão, e realmente espero que nada aconteça nessa parte com software, caso contrário, terei problemas. Então você precisa abordar isso. A segunda coisa é, lembre-se da Lei de Conway. Eu sugeriria, imprima, coloque em seu escritório, apenas para que todos se lembrem de que "não podemos projetar software isoladamente pensando nas estruturas da equipe".

...para realmente se beneficiar do microsserviço, você precisa fazer muito mais mudanças. Não é apenas a arquitetura técnica. É se você for um passo atrás, você precisa pensar na Lei de Conway, e como as estruturas de equipe são mapeadas com os serviços que você tem. Eles devem estar alinhados em grande parte, não um a um, mas devem estar alinhados. Caso contrário, você está lutando contra isso. Além disso, você já pensou em coisas como desacoplar equipes, mas também desacoplar ambientes se tiver ambientes estáticos para teste, desacoplar o processo de lançamento. Todos esses outros aspectos que você precisa considerar para realmente tirar o máximo proveito dos microsserviços nem sempre são pensados. Depois de fazer isso, acho que os microsserviços são realmente bons para garantir que estamos alinhando as equipes e os serviços com as áreas de negócios ou os fluxos de valor em nossos negócios. Isso pode ser muito poderoso.

Com a Lei de Conway, queremos que os limites do serviço, os limites da equipe estejam alinhados.

Maior desafio operacional com monólitos Noonan: À medida que voltamos para uma abordagem monolítica, acho que o maior desafio operacional com o qual lidamos agora é que, a qualquer momento em nosso trabalhador monolítico, estamos executando cerca de 2.000 a 4.000 trabalhadores. Isso significa que o cache na memória não é muito eficiente entre esses milhares de trabalhadores. Algo que introduzimos para nos ajudar com isso é o Redis. O Redis agora se tornou um ponto que devemos considerar toda vez que precisamos escalar. No passado, tivemos problemas em que o Redis ficava indisponível e os trabalhadores travavam. Isso agora adicionou um ponto adicional de escala para nós. É algo que vem surgindo consistentemente com o qual temos que lidar. Fizemos coisas diferentes, como mudar para o Redis Cluster, fragmentá-lo, mas ainda há algo em nossas mentes que gostaríamos que não existisse. Não basta voltarmos aos microsserviços apenas para obter o benefício do armazenamento em cache. É uma troca que estávamos dispostos e confortáveis ​​em aceitar.

Antever mudanças na organização: A funcionalidade do negócio evolui, assim como a estrutura da equipe. Como você casa isso com a estratégia de tecnologia? 
Como casar a evolução dos negócios e a estrutura da equipe com a tecnologia e a propriedade? 
O que vemos acontecer, e não é o que queremos, é que às vezes as decisões estão sendo tomadas, especialmente em torno das estruturas de equipe da organização, pelo pessoal de RH ou pela alta administração. Até certo ponto, devido ao efeito de espelhamento da Lei de Conway, eles estão decidindo sobre nossa arquitetura de software até certo ponto. Nós não queremos isso. O que estamos dizendo é que realmente precisamos unir esses dois mundos. Precisamos tomar decisões de tecnologia e design junto com as decisões de estrutura de equipe. Caso contrário, um está restringindo o que o outro é capaz de fazer.

Entender, profundamete, o efeito de espelhamento da Lei de Conway, à ponto de poder traçar bem os diferentes domínios de especialidade do negócio;
Descrever a proposta de captura de valor; Delinear proposta de valor do negócio; Criar estratégia de captura do valor; Criar arquitetura de solução; implementar o monitoramento contínuo;
Criar arquitetura de software alinhada aos bounded contexts; identificar gargalos técnicos; dimensionar soluções com base nos gargalos; segmentar as responsabilidades;