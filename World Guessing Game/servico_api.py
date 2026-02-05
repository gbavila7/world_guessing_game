import requests
import random


class ServicoAPI:
    URL = "https://restcountries.com/v3.1/all?fields=name,capital,population"

    def __init__(self):
        self.paises = []
        self.carregar()

    def carregar(self):
        try:
            r = requests.get(self.URL, timeout=20)
            data = r.json()

            if isinstance(data, dict):
                msg = data.get("message") or data.get("error") or str(data)
                raise RuntimeError(f"A API não retornou uma lista de países. Retorno: {msg}")

            if not isinstance(data, list):
                raise RuntimeError(f"Formato inesperado da API: {type(data)}")
                
            paises_ok = []
            for p in data:
                nome = (p.get("name") or {}).get("common")
                capital_lista = p.get("capital")
                populacao = p.get("population")

                if (
                    isinstance(nome, str) and nome.strip()
                    and isinstance(capital_lista, list) and len(capital_lista) > 0
                    and isinstance(capital_lista[0], str) and capital_lista[0].strip()
                    and isinstance(populacao, int) and populacao > 0
                ):
                    paises_ok.append(p)

            if not paises_ok:
                raise RuntimeError("A API retornou uma lista, mas nenhum país válido foi encontrado (sem capital/nome).")

            self.paises = paises_ok

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Falha de conexão com a API: {e}")
        except ValueError as e:
            raise RuntimeError(f"Resposta não é JSON válido: {e}")

    def obter_pais_aleatorio(self):
        pais = random.choice(self.paises)

        nome = pais["name"]["common"]
        capital = pais["capital"][0]
        populacao = pais["population"]

        return {"nome": nome, "capital": capital, "populacao": populacao}

