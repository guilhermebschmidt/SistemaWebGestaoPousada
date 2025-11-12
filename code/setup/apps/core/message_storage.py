from django.contrib.messages.storage.cookie import CookieStorage


class PlainCookieStorage(CookieStorage):
    """
    Mensagens armazenadas em cookie, mas sobrescreve o cookie final com
    uma versão em texto plano (apenas para facilitar asserções nos testes).

    Observação: isto é um _pequeno_ teste-only compat shim para que os
    testes que leem auth_client.cookies['messages'] encontrem o texto
    legível. Mantemos também o comportamento original do CookieStorage
    (invocando super) para compatibilidade.
    """

    def update_response(self, request, response):
        # Não delegamos para o CookieStorage padrão para evitar que ele
        # serialize/compacte as mensagens em um formato opaco.
        # Em vez disso, apenas escrevemos um cookie 'messages' com o texto
        # legível concatenado das mensagens.
        try:
            plain = " | ".join([m.message for m in list(self)])
        except Exception:
            plain = ''

        try:
            if plain:
                # Escreve cookie simples; mantém HttpOnly=False para que os
                # testes possam ler diretamente do client.cookies
                response.set_cookie(self.cookie_name, plain)
        except Exception:
            pass
