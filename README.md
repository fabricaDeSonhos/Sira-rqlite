# 🚀 SIRA - Sistema de Reservas Distribuído

Um sistema de reservas robusto, moderno e altamente escalável construído sobre uma arquitetura de banco de dados distribuída.

## 📝 Sobre o Projeto
O SIRA foi desenvolvido para gerenciar e reservar qualquer tipo de recurso físico ou lógico, como salas de aula, laboratórios, auditórios e frotas de veículos. O grande diferencial desta aplicação é a sua infraestrutura descentralizada, desenhada especificamente para garantir alta disponibilidade e evitar pontos únicos de falha. É a solução ideal para instituições com múltiplos polos, blocos ou campi.

## 🏗️ Arquitetura do Sistema
O sistema segue um modelo rigoroso de separação de responsabilidades em camadas para garantir que a aplicação possa crescer sem gargalos de performance:

* **Frontend (Interface):** Camada interativa, rápida e totalmente responsiva.
* **Backend (Rotas e Regras de Negócio):** API leve e estruturada de forma eficiente para lidar com requisições concorrentes.
* **Persistência de Dados:** Camada descentralizada que opera de forma distribuída para garantir a resiliência do ecossistema.

## 🛠️ Tecnologias Utilizadas
A escolha da stack tecnológica foca no perfeito equilíbrio entre produtividade, estabilidade e alta performance:

* **Frontend:** React com Next.js
* **Backend:** Python com Flask
* **Integração:** Mapeamento Objeto-Relacional (ORM) 
* **Banco de Dados:** rqlite (banco de dados SQL distribuído baseado no protocolo de consenso Raft)

## 📊 Estrutura de Dados Distribuída
Uma estrutura de dados distribuída (ou banco de dados distribuído) é um modelo de armazenamento onde as informações não ficam centralizadas em uma única máquina. Em vez disso, os dados são divididos, replicados e sincronizados através de vários servidores (nós) interconectados em uma rede. 

Na prática, isso elimina o "ponto único de falha". Se um dos servidores cair, perder a conexão ou passar por manutenção, os outros nós possuem cópias dos dados e assumem o trabalho instantaneamente. Isso garante que o sistema continue no ar, responsivo e com a integridade das informações totalmente protegida.

## 👥 Equipe de Desenvolvimento

**Docente:**
* Hylson

**Discentes:**
* Helder
* Gabriel Rodrigues
* André Vitor
* Manuela
* Yuri
* Dylan
* Andrey
* Gustavo Tramontin
