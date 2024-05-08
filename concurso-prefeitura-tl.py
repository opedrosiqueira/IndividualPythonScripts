# busca no diario oficial da prefeitura e no blog da prefeitura por qualquer coisa que possa ter a ver com o concurso que minha esposa prestou.

import argparse
import io
import logging
import os
import re
import sqlite3
import sys
import webbrowser
from datetime import datetime, timedelta
from urllib.request import urlopen

import requests
from lxml import html
from pypdf import PdfReader


def showmessage(a, href, text):
    msg = f"<p><a href='{href}'>{a}</a>: {text}</p>"
    logging.warning(f'{a}: {text} ({href})')
    global file
    file.write(msg)
    global found
    found = True


def prepararBanco(path="/home/pedro/Mega/CodingProjects/PythonScripts/db.sqlite"):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS dias_vistos(data text)")
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS date_ix ON dias_vistos (data)")
    cur.execute("CREATE TABLE IF NOT EXISTS dias_nao_vistos(data text)")
    return cur


def buscatextos(content):
    logging.info("Finding matches...")
    matches = []
    matches += re.findall(r"cargo.{0,10}professor de ensino fundamental", content, re.IGNORECASE)
    matches += re.findall(r"edita.{0,30}16.{0,30}2022", content, re.IGNORECASE)
    matches += re.findall(r"concurso.{0,255}lagoas", content, re.IGNORECASE)
    matches += re.findall(r"698494", content, re.IGNORECASE)
    matches += re.findall(r"beatriz matos", content, re.IGNORECASE)
    matches += re.findall(r"beatriz siqueira", content, re.IGNORECASE)
    return set(matches)


def pdf2text(pdfReader):
    logging.info("Converting to text...")
    content = ""
    for i in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[i]
        content += pageObj.extract_text()
    return content


def baixarpdf(url):
    logging.info("Downloading " + url + "...")
    response = requests.get(url)
    on_fly_mem_obj = io.BytesIO(response.content)
    return PdfReader(on_fly_mem_obj)


def buscaassomasul(beginDate=datetime.now(), endDate=datetime(2022, 5, 1)):
    while beginDate >= endDate:
        url = f"https://diariooficialms.com.br/?data={beginDate.day}/{beginDate.month}/{beginDate.year}"
        headers = {'x-requested-with': 'XMLHttpRequest'}
        response = requests.get(url, headers=headers)

        beginDate = beginDate-timedelta(days=1)

        pdfs = re.findall(r"http.*\.pdf", response.text, re.IGNORECASE)  # busca por links pdfs
        if len(pdfs) <= 0:
            logging.info(f"No pdf found on {beginDate+timedelta(days=1)}!")
            continue

        for pdf in pdfs:  # para cada link pdf
            pdf_file = baixarpdf(pdf)  # baixa o pdf
            content = pdf2text(pdf_file)  # converte o pdf para texto
            matches = buscatextos(content)  # busca pelos termos no texto
            if len(matches) > 0:
                showmessage(beginDate+timedelta(days=1), pdf, matches)
            else:
                logging.info(f"No matching texts in {pdf}!")


def mesExtensoParaNumero(mes):
    mes = mes.lower()
    if mes == 'janeiro':
        return 1
    elif mes == 'fevereiro':
        return 2
    elif mes == 'março':
        return 3
    elif mes == 'abril':
        return 4
    elif mes == 'maio':
        return 5
    elif mes == 'junho':
        return 6
    elif mes == 'julho':
        return 7
    elif mes == 'agosto':
        return 8
    elif mes == 'setembro':
        return 9
    elif mes == 'outubro':
        return 10
    elif mes == 'novembro':
        return 11
    elif mes == 'dezembro':
        return 12


def getDate(date):
    result = re.search(r".*?(\d+)\s+(.+)\s+(\d+)", date)
    return f"{result.group(3)}-{mesExtensoParaNumero(result.group(2)):02d}-{int(result.group(1)):02d}"


def removeExtraWhitespaces(text):
    return re.sub(r"\s+", " ", text.strip())  # remove espaços duplicados


def buscatreslagoasblog(
        beginDate=datetime.now().strftime('%Y-%m-%d'),
        endDate=(datetime.now()-timedelta(days=30)).strftime('%Y-%m-%d'),
        first=1, last=50):
    for page in range(first, last):
        doc = html.parse(urlopen(f'https://www.treslagoas.ms.gov.br/blog/page/{page}')).getroot()
        for div in doc.cssselect('div[class*="kl-blog-item-container"]'):
            date = getDate(removeExtraWhitespaces(div.cssselect('div[class*="kl-blog-item-meta"]')[0].text_content()))
            if (date < endDate):
                return 1
            if (date > beginDate):
                continue

            title = removeExtraWhitespaces(div.cssselect('div[class*="kl-blog-item-title"]')[0].text_content())
            content = removeExtraWhitespaces(div.cssselect('div[class*="kl-blog-item-content"]')[0].text_content())
            link = div.cssselect('a')[0].get('href')

            if re.search(r"concurso|professor|docente", title, re.IGNORECASE):
                showmessage(date, link, title)
            elif re.search(r"concurso|professor|docente", content, re.IGNORECASE):
                showmessage(date, link, content)
            else:
                logging.info(f"Nothing found on blog {link[32:]}...")


if __name__ == "__main__":
    global found
    found = False
    db_path = '/home/pedro/Mega/CodingProjects/PythonScripts/db.sqlite'
    log_path = '/home/pedro/Mega/CodingProjects/PythonScripts/debug.log'
    filename = '/tmp/concurso.html'
    if os.name == 'nt':
        db_path = r'D:\Mega\CodingProjects\PythonScripts\db.sqlite'
        log_path = r'D:\Mega\CodingProjects\PythonScripts\debug.log'
        filename = os.environ['tmp']+'\\concurso.html'

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

    banco = prepararBanco(db_path)

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", '--begin', help="begin date on format yyyy-mm-dd")
    parser.add_argument("-e", '--end', help="end date on format yyyy-mm-dd")
    parser.add_argument("-f", '--first', help="first page to search", type=int)
    parser.add_argument("-l", '--last', help="last page to search", type=int)
    args = parser.parse_args()

    begin = args.begin if args.begin else datetime.now().strftime('%Y-%m-%d')
    end = args.end
    first = args.first if args.first else 1
    last = args.last if args.last else 50

    result = banco.execute("SELECT data FROM dias_vistos ORDER BY data DESC LIMIT 1").fetchone()
    if end is None and result:
        end = result[0]  # último dia visto
    if end is None:
        end = (datetime.now()-timedelta(days=30)).strftime('%Y-%m-%d')

    if begin < end:
        tmp = begin
        begin = end
        end = tmp

    global file
    file = open(filename, 'w+')
    file.write(f"<h1>searching from {begin} to {end}</h1>")

    buscatreslagoasblog(begin, end, first, last)
    buscaassomasul(datetime.strptime(begin, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d'))

    if not found:
        file.write('<p>Nothing found today!</p>')
    file.close()

    webbrowser.open('file://'+os.path.abspath(filename), new=2)

    ontem = datetime.now()-timedelta(days=1)

    try:
        banco.execute(f"INSERT INTO dias_vistos VALUES ('{str(ontem)[:10]}')")
        banco.connection.commit()
    except sqlite3.IntegrityError:
        pass

# https://diariooficialms.com.br/media/75282/3217---17-11-22.pdf
# da katia 196 até a ana 235
