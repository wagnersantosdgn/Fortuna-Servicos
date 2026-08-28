# Fortuna Serviços

## 📋 Sobre o projeto

O **Fortuna Serviços** é uma plataforma voltada à terceirização de
serviços residenciais e domésticos, com o objetivo de facilitar a
localização e contratação de prestadores de serviços.

A plataforma permitirá que **clientes** encontrem profissionais e que
**prestadores** divulguem seus serviços, qualificações, preços e formas
de pagamento.

> **Projeto:** Terceirização de Serviços Residenciais & Domésticos\
> **Cliente/Área solicitante:** PF & PJ\
> **Versão:** 1.0\
> **Data de elaboração:** 29/07/2026\
> **Prazo desejado:** 28/08/2026

------------------------------------------------------------------------

## 🎯 Objetivo

Facilitar a localização de prestadores de serviços residenciais e
domésticos, permitindo a terceirização de demandas residenciais por meio
de uma plataforma web.

### Usuários envolvidos

-   **Cliente (Solicitante):** usuário que busca e contrata serviços.
-   **Prestador:** profissional que divulga e realiza serviços.

------------------------------------------------------------------------

## ⚙️ Requisitos Funcionais

  -------------------------------------------------------------------------------
  ID             Requisito         Ator/Perfil    Prioridade     Critério de
                                                                 Aceite
  -------------- ----------------- -------------- -------------- ----------------
  **RF-01**      Permitir a        Cliente /      Essencial      Senha e e-mail
                 realização de     Prestador                     devem estar
                 login.                                          dentro das
                                                                 políticas de
                                                                 aceite do site.

  **RF-02**      Permitir a        Cliente /      Essencial      O perfil deve
                 criação de        Prestador                     conter os dados
                 perfil.                                         completos do
                                                                 usuário.

  **RF-03**      Permitir a        Prestador      Essencial      O prestador deve
                 divulgação de                                   informar suas
                 serviços.                                       qualificações.

  **RF-04**      Permitir o        Cliente /      Essencial      Prestadores
                 cadastramento de  Prestador                     devem cadastrar
                 preços dos                                      os valores
                 serviços, formas                                cobrados pelos
                 de pagamento,                                   serviços.
                 agendamento e                                   
                 carrinho de                                     
                 compra para mais                                
                 de um serviço.                                  

  **RF-05**      Permitir chat     Cliente /      Desejável      O solicitante
                 para              Prestador                     poderá entrar em
                 intermediações.                                 contato com o
                                                                 prestador dentro
                                                                 do site.
  -------------------------------------------------------------------------------

------------------------------------------------------------------------

## 🛡️ Requisitos Não Funcionais

  -----------------------------------------------------------------------
  ID                Categoria         Requisito         Critério de
                                                        Verificação
  ----------------- ----------------- ----------------- -----------------
  **RNF-01**        Desempenho        A pesquisa deve   Verificação
                                      retornar em até   durante a
                                      **3 segundos**,   pesquisa
                                      com no máximo 20  realizada pelo
                                      pesquisas por     solicitante.
                                      página            
                                      encontrada.       

  **RNF-02**        Segurança / LGPD  Dados pessoais,   Dados armazenados
                                      como nome, e-mail no banco de dados
                                      e senha, devem    com controle
                                      ser tratados      adequado.
                                      conforme a LGPD,  
                                      com controle de   
                                      acesso por        
                                      perfil.           

  **RNF-03**        Usabilidade       Cada prestador    Avaliação de **0
                                      poderá ser        a 5**, coletada
                                      avaliado e terá   após a prestação
                                      uma nota exibida  do serviço.
                                      em seu perfil.    

  **RNF-04**        Disponibilidade   O site deverá     Sistema funcional
                                      permanecer        continuamente.
                                      disponível 24     
                                      horas por dia, 7  
                                      dias por semana.  

  **RNF-05**        Escalabilidade    A plataforma      Possibilidade de
                                      estará disponível localizar
                                      inicialmente para prestadores em
                                      todo o Brasil,    diferentes
                                      com filtro de     regiões do
                                      localização por   Brasil.
                                      região.           

  **RNF-06**        Compatibilidade   A plataforma      Site adaptável
                                      estará disponível aos diferentes
                                      via website, com  tipos de
                                      compatibilidade   dispositivos.
                                      com diferentes    
                                      dispositivos.     
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📐 Regras de Negócio

  -----------------------------------------------------------------------
  ID                Regra             Aplicada a        Referência
  ----------------- ----------------- ----------------- -----------------
  **RN-01**         Será cobrada uma  RF-03             Política da
                    taxa de **10%**                     empresa
                    sobre cada                          
                    serviço                             
                    contratado pela                     
                    plataforma.                         

  **RN-02**         Apenas            RF-02             Política da
                    profissionais com                   empresa
                    cadastro completo                   
                    e aprovado                          
                    poderão anunciar                    
                    serviços.                           

  **RN-03**         Apenas usuários   RF-01             Política da
                    cadastrados                         empresa
                    poderão contratar                   
                    serviços.                           

  **RN-04**         Após a conclusão  RF-05             Política da
                    do serviço,                         empresa
                    cliente e                           
                    profissional                        
                    poderão realizar                    
                    avaliações                          
                    mútuas.                             

  **RN-05**         Devem ser         RN-01             LGPD --- Art. 6º,
                    coletados apenas                    III
                    os dados mínimos                    
                    necessários para                    
                    o cadastramento e                   
                    funcionamento da                    
                    plataforma.                         

  **RN-06**         Deve existir um   RN-01             LGPD --- Art. 6º,
                    termo de aceite                     I e VI; Art. 8º
                    especificando a                     
                    coleta dos dados                    
                    e como eles serão                   
                    utilizados.                         
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🗂️ Estrutura de usuários

### Cliente

O cliente poderá:

-   Criar uma conta;
-   Criar e gerenciar seu perfil;
-   Pesquisar prestadores;
-   Consultar serviços;
-   Consultar preços;
-   Agendar serviços;
-   Adicionar mais de um serviço ao carrinho;
-   Realizar contratação;
-   Avaliar prestadores;
-   Utilizar o chat para intermediação.

### Prestador

O prestador poderá:

-   Criar uma conta;
-   Criar e completar seu perfil;
-   Informar qualificações;
-   Divulgar serviços;
-   Definir preços;
-   Informar formas de pagamento;
-   Gerenciar agendamentos;
-   Receber avaliações;
-   Utilizar o chat para intermediação.

------------------------------------------------------------------------

## ⭐ Sistema de avaliações

Após a conclusão de um serviço, cliente e profissional poderão realizar
avaliações mútuas.

A avaliação dos prestadores utilizará uma escala de:

**0 a 5 estrelas/notas**

A nota ficará disponível no perfil do prestador para auxiliar os
solicitantes na escolha de profissionais recomendados.

------------------------------------------------------------------------

## 🔐 Segurança e LGPD

A plataforma deverá tratar os dados pessoais dos usuários de acordo com
a **Lei Geral de Proteção de Dados (LGPD)**.

Entre os dados mencionados no levantamento estão:

-   Nome;
-   E-mail;
-   Senha.

O sistema deverá possuir controle de acesso por perfil e coletar somente
os dados necessários para o funcionamento da plataforma.

Também deverá existir um **termo de aceite/política de privacidade**
informando quais dados são coletados e como serão utilizados.

------------------------------------------------------------------------

## 📍 Localização

A plataforma será disponibilizada inicialmente para todo o **Brasil**.

O sistema deverá oferecer recursos de localização para que o usuário
consiga encontrar prestadores por região, possibilitando a identificação
de profissionais mais próximos.

------------------------------------------------------------------------

## 📊 Prioridade dos requisitos

  -----------------------------------------------------------------------
  Prioridade                          Significado
  ----------------------------------- -----------------------------------
  **Essencial**                       Sem esse requisito, o sistema não
                                      atende ao objetivo do projeto
                                      (MVP).

  **Importante**                      Agrega valor significativo, mas
                                      pode ser entregue em uma fase
                                      posterior.

  **Desejável**                       Funcionalidade complementar, sem
                                      impacto crítico caso esteja
                                      ausente.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧩 Categorias de requisitos não funcionais

-   **Desempenho:** tempo de resposta, throughput e uso de recursos.
-   **Segurança:** autenticação, autorização, criptografia e proteção de
    dados.
-   **Usabilidade:** facilidade de uso e acessibilidade.
-   **Disponibilidade:** tempo em que o sistema permanece operacional.
-   **Escalabilidade:** capacidade de suportar aumento de usuários,
    dados e transações.
-   **Compatibilidade:** funcionamento em diferentes sistemas,
    navegadores e dispositivos.
-   **Manutenibilidade:** facilidade de manutenção, atualização e
    correção.
-   **Confiabilidade:** tolerância a falhas, consistência, backup e
    recuperação.

------------------------------------------------------------------------

## 👥 Responsáveis

  Nome                  Papel / Área             Data
  --------------------- ------------------------ ------------
  **Cleidson Amorim**   Solicitante / Cliente    28/08/2026
  **Carlos Henrique**   Dev FrontEnd             29/07/2026
  **Paulo Rogério**     Dev DBA                  29/07/2026
  **Carlos Mol**        Dev BackEnd              29/07/2026
  **Wagner Santos**     Tech Lead & QA           29/07/2026

------------------------------------------------------------------------

## 📌 Status

**Versão atual:** 1.0

O documento de requisitos deve ser revisado e validado pelas partes
interessadas antes do início do desenvolvimento. Alterações posteriores
devem ser registradas em uma nova versão do documento.
