# Steam Market Scraper

Este projeto é um web scraper para coletar dados de preços de itens no mercado da Steam.

## 📌 Funcionalidades
- Coleta informações de preços de itens no mercado da Steam.
- Utiliza `requests` e `BeautifulSoup` para extrair os dados.
- Trata erros e limita requisições para evitar bloqueios da Steam.
- Permite personalizar as URLs a serem buscadas.
- Salva os dados coletados para análise posterior.

## 🛠 Requisitos
Antes de rodar o scraper, instale as dependências necessárias:
```bash
pip install requests beautifulsoup4
```

## 🚀 Como Usar
1. Clone este repositório:
```bash
git clone https://github.com/forever-prata/SteamWebScrapper.git
```
2. Navegue até a pasta do projeto:
```bash
cd steam-market-scraper
```
3. Edite o arquivo `urls.txt` para adicionar as URLs dos itens que deseja buscar.
```bash
urls = [
    "https://steamcommunity.com/market/listings/730/Item1",
    "https://steamcommunity.com/market/listings/730/Item2"
]
```
4. Execute o script:
```bash
python scraper.py
```

## ⚠️ Considerações
- A Steam pode bloquear requisições excessivas. Recomenda-se ajustar a frequência das requisições.
- Para evitar bloqueios, utilize proxies e altere o `User-Agent`.
- Verifique a legalidade do scraping conforme os termos de uso da Steam.

## 📄 Licença
Este projeto está sob a licença MIT. Sinta-se livre para modificar e compartilhar.
