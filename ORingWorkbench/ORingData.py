# -*- coding: utf-8 -*-

# ORingData.py
# Camada de dados da ORingWorkbench.
# Fontes (normalizadas a partir dos catalogos FamaFlex / Parker / Smierveda, ISO 3601):
#   o-ring_pol.csv  - tamanhos padrao AS568 (polegadas + mm equivalentes), chave = as568
#   o-ring_mm.csv   - tamanhos metricos, chave = designacao (di x w)
#   material.csv    - catalogo de materiais (polimero/dureza/temperatura)
#   brand.csv       - referencia de fabricante: codigo -> tamanho padrao + material

import csv
import os


def _parse_float(value):
    """Converte valor com virgula decimal para float. Retorna None se vazio."""
    if value is None:
        return None
    value = value.strip().replace(",", ".")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


class ORingRecord:
    """Registro unico de o-ring (visao denormalizada para dialogo/API)."""

    def __init__(self, key, catalogo, tabela, codigo, referencia, norma,
                 di_interno, tolerancia_di, secao_w, tolerancia_w,
                 de_externo, material, polimero, dureza_shore_a, temperatura):
        self.key = key
        self.catalogo = catalogo
        self.tabela = tabela
        self.codigo = codigo
        self.referencia = referencia
        self.norma = norma
        self.di_interno = di_interno
        self.tolerancia_di = tolerancia_di
        self.secao_w = secao_w
        self.tolerancia_w = tolerancia_w
        self.de_externo = de_externo
        self.material = material
        self.polimero = polimero
        self.dureza_shore_a = dureza_shore_a
        self.temperatura = temperatura

    @property
    def major_radius(self):
        """Raio medio do toro: (di_interno + secao) / 2."""
        return (self.di_interno + self.secao_w) / 2.0

    @property
    def minor_radius(self):
        """Raio da secao transversal: secao_w / 2."""
        return self.secao_w / 2.0

    def __repr__(self):
        return f"ORingRecord(key={self.key!r}, di={self.di_interno}, w={self.secao_w})"


class ORingData:
    """Carrega, valida e consulta os dados de o-rings normalizados."""

    def __init__(self, data_dir=None):
        self.data_dir = data_dir or os.path.dirname(os.path.realpath(__file__))
        self.records = []
        self.errors = []
        self.materials = {}
        self.as568 = {}
        self.metric = {}

        self._load()

    def _read_csv(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f, delimiter=";"))

    def _load_materials(self):
        for row in self._read_csv("material.csv"):
            name = (row.get("material") or "").strip()
            if not name:
                continue
            self.materials[name] = {
                "polimero": (row.get("polimero") or "").strip(),
                "dureza_shore_a": (row.get("dureza_shore_a") or "").strip(),
                "temperatura": (row.get("temperatura_c") or "").strip(),
            }

    def _load_sizes(self):
        for row in self._read_csv("o-ring_pol.csv"):
            dash = (row.get("as568") or "").strip()
            self.as568[dash] = {
                "di": _parse_float(row.get("di_interno_mm")),
                "w": _parse_float(row.get("secao_w_mm")),
                "de": _parse_float(row.get("de_externo_mm")),
                "tol_di": _parse_float(row.get("tolerancia_di_mm")),
                "tol_w": _parse_float(row.get("tolerancia_w_mm")),
            }
        for row in self._read_csv("o-ring_mm.csv"):
            ref = (row.get("designacao") or "").strip()
            self.metric[ref] = {
                "di": _parse_float(row.get("di_interno_mm")),
                "w": _parse_float(row.get("secao_w_mm")),
                "de": _parse_float(row.get("de_externo_mm")),
                "tol_di": _parse_float(row.get("tolerancia_di_mm")),
                "tol_w": _parse_float(row.get("tolerancia_w_mm")),
            }

    def _load_brands(self):
        for row in self._read_csv("brand.csv"):
            fabricante = (row.get("fabricante") or "").strip()
            codigo = (row.get("codigo") or "").strip()
            referencia = (row.get("referencia") or "").strip()
            material = (row.get("material") or "").strip()
            tabela = (row.get("tabela") or "").strip()

            if referencia in self.as568:
                size, norma = self.as568[referencia], "AS568"
            elif referencia in self.metric:
                size, norma = self.metric[referencia], "ISO 3601"
            else:
                self.errors.append(
                    f"Referencia nao resolvida: fabricante={fabricante}, codigo={codigo or '-'}, ref={referencia}")
                continue

            di, w, de = size["di"], size["w"], size["de"]
            if di is None or w is None:
                self.errors.append(f"Tamanho invalido: fabricante={fabricante}, ref={referencia}")
                continue

            if codigo:
                key = f"{fabricante}|{codigo}"
            else:
                key = f"{fabricante}|metrico|{di}|{w}"

            mat = self.materials.get(material, {})
            record = ORingRecord(
                key=key,
                catalogo=fabricante,
                tabela=tabela,
                codigo=codigo,
                referencia=referencia,
                norma=norma,
                di_interno=di,
                tolerancia_di=size["tol_di"],
                secao_w=w,
                tolerancia_w=size["tol_w"],
                de_externo=de,
                material=material,
                polimero=mat.get("polimero", ""),
                dureza_shore_a=mat.get("dureza_shore_a", ""),
                temperatura=mat.get("temperatura", ""),
            )
            self.records.append(record)

    def _load(self):
        self._load_materials()
        self._load_sizes()
        self._load_brands()

    def get_record(self, key):
        for record in self.records:
            if record.key == key:
                return record
        raise ValueError(f"O-Ring '{key}' nao encontrado na base de dados.")

    def find(self, **kwargs):
        """Busca por atributos (ex.: find(catalogo='Parker'))."""
        results = []
        for record in self.records:
            matches = True
            for attr, value in kwargs.items():
                if getattr(record, attr, None) != value:
                    matches = False
                    break
            if matches:
                results.append(record)
        return results

    def __len__(self):
        return len(self.records)
