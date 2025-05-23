
# 🏛️ Bot de Automação de IPTU – Download de PDFs e Extração de Dados

Este projeto é um bot de automação feito com **Selenium e Python** que acessa o site da prefeitura da sua cidade, **pesquisa imóveis com base em uma lista de códigos**, baixa os arquivos PDF com as guias de IPTU e depois **extrai as informações relevantes** desses documentos, gerando uma planilha CSV consolidada.

---

## ⚠️ Aviso

Este repositório **não contém dados reais de terceiros**. Os arquivos presentes (`iptus.csv`, PDFs, etc.) foram gerados com **dados fictícios apenas para fins demonstrativos**.

Se você deseja rodar o projeto com seus próprios dados, substitua o conteúdo desses arquivos localmente — nunca exponha dados pessoais ou sensíveis em repositórios públicos.

---

## ✅ O que este projeto faz

1. **Lê uma lista de códigos de imóveis** a partir de um arquivo CSV.
2. **Usa o Selenium** para acessar o site da prefeitura e fazer as pesquisas.
3. **Baixa os PDFs de IPTU** de cada imóvel.
4. **Usa pdfplumber** para abrir os PDFs (inclusive os com várias páginas) e extrair dados como:
   - Linha digitável
   - Nosso número
   - Data de vencimento
   - Número do documento
5. **Gera um arquivo CSV** com todos esses dados organizados.

---

## 📁 Estrutura do Projeto

```
backend/
├── iptus.csv                             # Planilha com dados fictícios
├── emission_pdfs_iptu/
│   └── pdfs_iptu/                        # PDFs fictícios ou simulados
├── extracao_dados_pdf/
│   ├── extract.py                        # Código para ler os PDFs e extrair dados
│   └── generate_csv.py                   # Gera o CSV a partir dos dados extraídos
└── main.py                               # Script principal que faz toda a automação
```

---

## 🧰 Requisitos

- Python 3.10+
- Google Chrome + ChromeDriver (para o Selenium funcionar)
- Instalar as dependências com:

```bash
pip install selenium pdfplumber
```

---

## ▶️ Como usar

1. **Prepare a lista de códigos de imóveis** no arquivo CSV que será usado (por exemplo, `iptus.csv`).
2. **Execute o script principal** para iniciar a automação:

```bash
python main.py
```

3. **Após o download dos PDFs**, execute o script para gerar o CSV com os dados extraídos:

```bash
cd backend/extracao_dados_pdf
python generate_csv.py
```

4. O arquivo `iptus.csv` será criado com todas as informações organizadas.

---

## 📊 Dados extraídos

O sistema identifica automaticamente múltiplas páginas por guia e cria colunas dinâmicas como:

- `linha_digitavel_1`, `linha_digitavel_2`, ...
- `nosso_numero_1`, `nosso_numero_2`, ...
- `data_vencimento_1`, `data_vencimento_2`, ...
- `numero_documento_1`, `numero_documento_2`, ...

---

## 📌 Observações

- Os PDFs devem conter **texto pesquisável** (não podem ser apenas imagens).
- A extração usa expressões regulares para localizar os dados nas páginas.
- Verifique se a versão do **ChromeDriver** é compatível com a versão do seu Google Chrome.

---

**Desenvolvido para automatizar o processo de emissão e controle de guias de IPTU em grande escala.**
