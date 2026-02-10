WikiCircuito PRO

O WikiCircuito PRO é uma aplicação web desenvolvida em Python com Streamlit, voltada para ambientes educacionais (laboratórios escolares e técnicos).
Ela permite o gerenciamento e a visualização de projetos eletrônicos, componentes, QR Codes e estoque, com funcionalidades diferentes para Aluno e Técnico.

🚀 Funcionalidades
👨‍🎓 Perfil Aluno

Login seguro

Visualização de projetos do laboratório

Busca de projetos por componente

Leitura e visualização de QR Codes

Descrição simples dos componentes

Botão “Esqueceu a senha?”

Logout com confirmação

🧑‍🔧 Perfil Técnico

Todas as funções do aluno

Cadastro de novos projetos

Controle de estoque de componentes

Visualização completa dos componentes

Geração automática de QR Codes

Logout com confirmação

🖥️ Tecnologias Utilizadas

Python 3

Streamlit

Pandas

QRCode

JSON (armazenamento de dados)

HTML/CSS (customização visual)

📂 Estrutura de Arquivos
📁 wikicircuito/
├── wikicircuito.py       # Código principal da aplicação
├── usuarios.json         # Usuários do sistema
├── projetos.json         # Projetos cadastrados
├── historico.json        # Histórico de buscas dos alunos
├── estoque.json          # Controle de estoque
└── README.md             # Documentação do projeto

🔐 Usuários Padrão
Usuário	Senha	Perfil
aluno	123	Aluno
tecnico	123	Técnico

⚠️ Recomenda-se alterar as senhas em ambiente real.

▶️ Como Executar o Projeto
1️⃣ Instale as dependências
pip install streamlit pandas qrcode pillow

2️⃣ Execute a aplicação
streamlit run wikicircuito.py

3️⃣ Acesse no navegador
http://localhost:8501/

📸 Interface

Interface moderna com tema escuro

Cards animados para projetos

Sidebar dinâmica por perfil

Layout responsivo (wide)

📦 Armazenamento de Dados

Os dados são salvos localmente em arquivos .json, facilitando:

Portabilidade

Manutenção

Uso educacional sem banco de dados

🎯 Objetivo Educacional

O WikiCircuito ULTRA foi criado para:

Auxiliar alunos no aprendizado de eletrônica

Organizar projetos de laboratório

Incentivar o uso de QR Codes em ambientes educacionais

Facilitar a gestão de componentes por técnicos

🧠 Próximas Melhorias (Ideias)

Cadastro de imagens dos projetos

Níveis de permissão avançados

Integração com banco de dados

Exportação de relatórios em PDF

Leitura de QR Code por câmera

👨‍💻 Autor

Projeto desenvolvido para fins educacionais, com foco em aprendizado prático, organização de laboratório e tecnologia aplicada à educação.
