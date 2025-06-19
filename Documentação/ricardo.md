# Estrutura do Projeto Django - Documentação Técnica

## 📌 Visão Geral

Este projeto Django adota uma arquitetura baseada em um único app principal chamado `core`, que agrupa todas as entidades do sistema: `Hospede`, `Quarto` e `Reserva`. Dentro do app `core`, o código é organizado por responsabilidade (models, views, forms, urls), com separação clara por entidade em cada pasta.

---

## 🛠️ Justificativa da Refatoração

Inicialmente, o projeto foi estruturado com múltiplos apps distintos, como `hospede`, `quarto`, e `reserva`. No entanto, essa organização começou a gerar problemas à medida que o sistema crescia:

- **Dispersão de arquivos**: Muitos arquivos pequenos espalhados por apps distintos tornavam a navegação e o entendimento mais difíceis.
- **Interdependência entre apps**: As entidades tinham forte ligação entre si, o que tornava artificial sua separação.
- **Migrações complexas**: Alterações envolvendo múltiplas entidades exigiam sincronização de migrações entre apps.
- **Carga cognitiva alta**: Desenvolvedores precisavam alternar constantemente entre apps para alterações simples.

Diante disso, optamos por consolidar a estrutura em um único app `core`, melhorando a coesão e simplificando a manutenção.

---

## 🗂️ Estrutura Atual

```plaintext
apps/
└── core/
    ├── models/
    │   ├── hospede.py
    │   ├── quarto.py
    │   └── reserva.py
    ├── forms/
    │   ├── hospede.py
    │   ├── quarto.py
    │   └── reserva.py
    ├── views/
    │   ├── hospede.py
    │   ├── quarto.py
    │   └── reserva.py
    ├── urls/
    │   ├── hospede.py
    │   ├── quarto.py
    │   └── reserva.py
    ├── admin.py
    ├── apps.py
    ├── urls.py
    └── views.py
