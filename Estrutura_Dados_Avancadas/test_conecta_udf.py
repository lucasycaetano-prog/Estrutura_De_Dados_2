"""Testes automatizados do projeto ConectaUDF (biblioteca padrão)."""

import unittest

from conecta_udf import (
    REDE_ORIGINAL,
    NOVAS_AMIZADES,
    amigos_em_comum,
    ampliar_rede,
    densidade,
    graus,
    menor_caminho,
    sugestoes_de_amizade,
    total_arestas,
    validar_rede,
)


class TestConectaUDF(unittest.TestCase):
    def setUp(self):
        self.expandida = ampliar_rede(
            REDE_ORIGINAL,
            ["Gabriela", "Henrique", "Isabela", "João"],
            NOVAS_AMIZADES,
        )

    def test_rede_original(self):
        validar_rede(REDE_ORIGINAL)
        self.assertEqual(len(REDE_ORIGINAL), 6)
        self.assertEqual(
            graus(REDE_ORIGINAL),
            {"Ana": 2, "Bruno": 3, "Carla": 3, "Diego": 3, "Elisa": 3, "Felipe": 2},
        )
        self.assertEqual(sum(graus(REDE_ORIGINAL).values()), 16)
        self.assertEqual(total_arestas(REDE_ORIGINAL), 8)
        self.assertAlmostEqual(densidade(REDE_ORIGINAL), 8 / 15)

    def test_caminhos(self):
        caminho = menor_caminho(REDE_ORIGINAL, "Ana", "Felipe")
        self.assertEqual(caminho, ["Ana", "Bruno", "Diego", "Felipe"])
        self.assertEqual(len(caminho) - 1, 3)
        alternativo = ["Ana", "Carla", "Elisa", "Felipe"]
        self.assertTrue(all(b in REDE_ORIGINAL[a] for a, b in zip(alternativo, alternativo[1:])))
        self.assertEqual(len(alternativo) - 1, 3)

    def test_rede_ampliada(self):
        validar_rede(self.expandida)
        self.assertEqual(len(self.expandida), 10)
        self.assertEqual(len(NOVAS_AMIZADES), 8)
        self.assertEqual(total_arestas(self.expandida), 16)
        self.assertEqual(sum(graus(self.expandida).values()), 32)
        self.assertEqual(
            graus(self.expandida),
            {"Ana": 3, "Bruno": 5, "Carla": 3, "Diego": 5,
             "Elisa": 4, "Felipe": 4, "Gabriela": 2, "Henrique": 2,
             "Isabela": 2, "João": 2},
        )
        self.assertAlmostEqual(densidade(self.expandida), 16 / 45)
        self.assertLess(densidade(self.expandida), densidade(REDE_ORIGINAL))
        self.assertEqual(REDE_ORIGINAL["Ana"], ["Bruno", "Carla"])

    def test_recomendacao(self):
        self.assertEqual(amigos_em_comum(self.expandida, "Bruno", "Elisa"), ["Carla", "Diego"])
        sugestoes = sugestoes_de_amizade(self.expandida)
        self.assertTrue(sugestoes)
        self.assertEqual(len(sugestoes[0][2]), 2)
        for a, b, _ in sugestoes:
            self.assertNotIn(b, self.expandida[a])

    def test_rejeita_amizade_invalida(self):
        rede_invalida = {"Ana": ["Bruno"], "Bruno": []}
        with self.assertRaises(ValueError):
            validar_rede(rede_invalida)
        with self.assertRaises(ValueError):
            ampliar_rede(REDE_ORIGINAL, [], [("Ana", "Bruno")])


if __name__ == "__main__":
    unittest.main()
