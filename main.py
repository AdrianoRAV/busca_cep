# # import flet as ft
# # import mysql.connector
# # from datetime import datetime
# # import requests
# # import base64
# # import json
# # from typing import Optional
# #
# #
# # # Classe da API dos Correios (mantida do seu código)
# # class CorreiosAPI:
# #     def __init__(self):
# #         self.url_token = "https://api.correios.com.br/token/v1/autentica"
# #         self.url_rastreamento = "https://api.correios.com.br/srorastrointerno/v2/rastros"
# #         self.auth_header = "Basic NTY3MToxNjU3MTYxMA=="
# #         self.token = None
# #
# #     def get_token(self) -> str:
# #         headers = {
# #             "Connection": "keep-alive",
# #             "Authorization": self.auth_header
# #         }
# #         try:
# #             response = requests.post(self.url_token, headers=headers)
# #             response.raise_for_status()
# #             data = response.json()
# #             self.token = data.get("token")
# #             return self.token
# #         except Exception as e:
# #             print(f"Erro ao obter token: {e}")
# #             return None
# #
# #     def consultar_rastreamento(self, codigo_rastreamento: str) -> Optional[dict]:
# #         if not self.token:
# #             self.get_token()
# #
# #         if not self.token:
# #             print("Erro: sem token.")
# #             return None
# #
# #         params = {
# #             "texto": "I",
# #             "resultado": "T",
# #             "codigosObjetos": codigo_rastreamento
# #         }
# #
# #         headers = {
# #             "Connection": "keep-alive",
# #             "Authorization": f"Bearer {self.token}"
# #         }
# #
# #         try:
# #             response = requests.get(self.url_rastreamento, params=params, headers=headers)
# #             response.raise_for_status()
# #             return response.json()
# #         except Exception as e:
# #             print(f"Erro na consulta ({codigo_rastreamento}): {e}")
# #             return None
# #
# #     def extrair_cep_destinatario(self, dados: dict) -> Optional[str]:
# #         try:
# #             objetos = dados.get("objetos", [])
# #             if not objetos:
# #                 return None
# #
# #             eventos = objetos[0].get("eventos", [])
# #             for ev in eventos:
# #                 if ev.get("codigo") == "PO":
# #                     cep = ev.get("destinatario", {}).get("endereco", {}).get("cep")
# #                     return cep
# #             return None
# #         except:
# #             return None
# #
# #     def get_cep_destinatario(self, codigo: str) -> Optional[str]:
# #         print(f"\n🔍 Consultando CEP para {codigo}")
# #         dados = self.consultar_rastreamento(codigo)
# #         if not dados:
# #             return None
# #         return self.extrair_cep_destinatario(dados)
# #
# #
# # # Função para conectar ao banco de dados
# # def conectar_banco():
# #     return mysql.connector.connect(
# #         host="10.87.199.29",
# #         user="sci_app",
# #         password="@sci_app",
# #         database="sci"
# #     )
# #
# #
# # # Função principal da aplicação Flet
# # def main(page: ft.Page):
# #     page.title = "Sistema de Registro de Objetos"
# #     page.theme_mode = ft.ThemeMode.LIGHT
# #     page.window_width = 800
# #     page.window_height = 600
# #     page.vertical_alignment = ft.MainAxisAlignment.CENTER
# #     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
# #
# #     # Variáveis globais
# #     registros = []
# #     api_correios = CorreiosAPI()
# #
# #     # Componentes da interface
# #     titulo = ft.Text(
# #         "📦 Sistema de Registro de Objetos",
# #         size=28,
# #         weight=ft.FontWeight.BOLD,
# #         color=ft.Colors.BLUE_800
# #     )
# #
# #     subtitulo = ft.Text(
# #         "Bipe o código do objeto para registrar no sistema",
# #         size=16,
# #         color=ft.Colors.GREY_600
# #     )
# #
# #
# #     # Campo de entrada para código
# #     codigo_input = ft.TextField(
# #         label="Código do Objeto",
# #         hint_text="Digite ou bipe o código de rastreamento",
# #         width=400,
# #         #autofocus=True,
# #         prefix_icon=ft.Icons.QUEUE_OUTLINED,
# #         text_size=16,
# #         border_color=ft.Colors.BLUE_400,
# #         on_submit=lambda e: registrar_codigo()
# #     )
# #
# #     # Botão de registro
# #     btn_registrar = ft.ElevatedButton(
# #         text="Registrar Código",
# #         icon=ft.Icons.ADD_CIRCLE_OUTLINED,
# #         on_click=lambda e: registrar_codigo(),
# #         width=200,
# #         height=50,
# #         style=ft.ButtonStyle(
# #             bgcolor=ft.Colors.BLUE_600,
# #             color=ft.Colors.WHITE
# #         )
# #     )
# #
# #     # Botão para buscar CEP
# #     btn_buscar_cep = ft.ElevatedButton(
# #         text="Buscar CEP do Último",
# #         icon=ft.Icons.SEARCH,
# #         on_click=lambda e: buscar_cep_ultimo(),
# #         width=200,
# #         height=50,
# #         style=ft.ButtonStyle(
# #             bgcolor=ft.Colors.GREEN_600,
# #             color=ft.Colors.WHITE
# #         )
# #     )
# #
# #     # Botão para processar lote
# #     btn_processar_lote = ft.ElevatedButton(
# #         text="Processar Lote",
# #         icon=ft.Icons.PLAY_ARROW,
# #         on_click=lambda e: processar_lote(),
# #         width=200,
# #         height=50,
# #         style=ft.ButtonStyle(
# #             bgcolor=ft.Colors.ORANGE_600,
# #             color=ft.Colors.WHITE
# #         )
# #     )
# #
# #     # Lista de registros
# #     lista_registros = ft.ListView(
# #         expand=True,
# #         spacing=10,
# #         padding=20
# #     )
# #
# #     # Mensagem de status
# #     status_snackbar = ft.SnackBar(content=ft.Text(""))
# #
# #     # Função para registrar código no banco
# #     def registrar_codigo():
# #         codigo = codigo_input.value.strip()
# #
# #         if not codigo:
# #             mostrar_mensagem("❌ Digite um código válido!", ft.Colors.RED)
# #             return
# #
# #         try:
# #             # Conectar ao banco
# #             db = conectar_banco()
# #             cursor = db.cursor()
# #
# #             # Verificar se código já existe
# #             cursor.execute("SELECT id FROM tb_obj_registrado WHERE codigo = %s", (codigo,))
# #             if cursor.fetchone():
# #                 mostrar_mensagem("⚠️ Código já registrado!", ft.Colors.ORANGE)
# #                 return
# #
# #             # Inserir novo registro
# #             sql = "INSERT INTO tb_obj_registrado (codigo, data_registro) VALUES (%s, %s)"
# #             valores = (codigo, datetime.now())
# #             cursor.execute(sql, valores)
# #             db.commit()
# #
# #             # Atualizar lista
# #             carregar_registros()
# #
# #             # Limpar campo
# #             codigo_input.value = ""
# #
# #             mostrar_mensagem(f"✅ Código {codigo} registrado com sucesso!", ft.Colors.GREEN)
# #
# #             cursor.close()
# #             db.close()
# #
# #         except Exception as e:
# #             mostrar_mensagem(f"❌ Erro ao registrar: {str(e)}", ft.Colors.RED)
# #
# #     # Função para buscar CEP do último registro
# #     def buscar_cep_ultimo():
# #         try:
# #             db = conectar_banco()
# #             cursor = db.cursor(dictionary=True)
# #
# #             # Buscar último registro
# #             cursor.execute("SELECT codigo FROM tb_obj_registrado ORDER BY id DESC LIMIT 1")
# #             ultimo = cursor.fetchone()
# #
# #             if not ultimo:
# #                 mostrar_mensagem("❌ Nenhum registro encontrado!", ft.Colors.RED)
# #                 return
# #
# #             codigo = ultimo['codigo']
# #             cep = api_correios.get_cep_destinatario(codigo)
# #
# #             if cep:
# #                 resultado = f"{codigo}{cep}"
# #                 with open("resultado.txt", "a", encoding="utf-8") as arquivo:
# #                     arquivo.write(resultado + "\n")
# #                 mostrar_mensagem(f"✅ CEP encontrado: {cep} para {codigo}", ft.Colors.GREEN)
# #             else:
# #                 mostrar_mensagem(f"❌ CEP não encontrado para {codigo}", ft.Colors.ORANGE)
# #
# #             cursor.close()
# #             db.close()
# #
# #         except Exception as e:
# #             mostrar_mensagem(f"❌ Erro ao buscar CEP: {str(e)}", ft.Colors.RED)
# #
# #     # Função para processar lote
# #     def processar_lote():
# #         try:
# #             db = conectar_banco()
# #             cursor = db.cursor(dictionary=True)
# #
# #             cursor.execute("SELECT id, codigo FROM tb_obj_registrado")
# #             registros = cursor.fetchall()
# #
# #             if not registros:
# #                 mostrar_mensagem("❌ Nenhum registro para processar!", ft.Colors.RED)
# #                 return
# #
# #             progresso = ft.ProgressBar(width=400, color=ft.Colors.BLUE)
# #             progresso_container = ft.Container(
# #                 content=progresso,
# #                 padding=10
# #             )
# #
# #             page.add(progresso_container)
# #             page.update()
# #
# #             processados = 0
# #             total = len(registros)
# #
# #             for reg in registros:
# #                 codigo = reg["codigo"]
# #                 cep = api_correios.get_cep_destinatario(codigo)
# #
# #                 if cep:
# #                     resultado = f"{codigo}{cep}"
# #                     with open("resultado.txt", "a", encoding="utf-8") as arquivo:
# #                         arquivo.write(resultado + "\n")
# #                     processados += 1
# #
# #                 progresso.value = processados / total
# #                 page.update()
# #
# #             page.remove(progresso_container)
# #             mostrar_mensagem(f"✅ Processamento concluído! {processados}/{total} objetos", ft.Colors.GREEN)
# #
# #             cursor.close()
# #             db.close()
# #
# #         except Exception as e:
# #             mostrar_mensagem(f"❌ Erro ao processar lote: {str(e)}", ft.Colors.RED)
# #
# #     # Função para carregar registros
# #     def carregar_registros():
# #         try:
# #             lista_registros.controls.clear()
# #
# #             db = conectar_banco()
# #             cursor = db.cursor(dictionary=True)
# #
# #             cursor.execute("SELECT id, codigo, data_registro FROM tb_obj_registrado ORDER BY id DESC LIMIT 50")
# #             registros = cursor.fetchall()
# #
# #             if not registros:
# #                 lista_registros.controls.append(
# #                     ft.ListTile(
# #                         title=ft.Text("Nenhum registro encontrado"),
# #                         leading=ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.GREY)
# #                     )
# #                 )
# #             else:
# #                 for reg in registros:
# #                     data_formatada = reg['data_registro'].strftime("%d/%m/%Y %H:%M:%S")
# #                     lista_registros.controls.append(
# #                         ft.Card(
# #                             content=ft.Container(
# #                                 content=ft.ListTile(
# #                                     leading=ft.Icon(ft.Icons.LOCAL_SHIPPING, color=ft.Colors.BLUE),
# #                                     title=ft.Text(f"Código: {reg['codigo']}"),
# #                                     subtitle=ft.Text(f"ID: {reg['id']} | Data: {data_formatada}"),
# #                                     trailing=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
# #                                 ),
# #                                 padding=10
# #                             )
# #                         )
# #                     )
# #
# #             cursor.close()
# #             db.close()
# #             page.update()
# #
# #         except Exception as e:
# #             mostrar_mensagem(f"Erro ao carregar registros: {str(e)}", ft.Colors.RED)
# #
# #     # Função para mostrar mensagens
# #     def mostrar_mensagem(mensagem, cor):
# #         status_snackbar.content = ft.Text(mensagem)
# #         status_snackbar.bgcolor = cor
# #         status_snackbar.open = True
# #         page.update()
# #
# #     # Layout da página
# #     page.add(
# #         ft.Container(
# #             content=ft.Column(
# #                 [
# #                     ft.Row([titulo], alignment=ft.MainAxisAlignment.CENTER),
# #                     ft.Row([subtitulo], alignment=ft.MainAxisAlignment.CENTER),
# #
# #                     ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
# #
# #                     ft.Row(
# #                         [codigo_input],
# #                         alignment=ft.MainAxisAlignment.CENTER
# #                     ),
# #
# #                     ft.Row(
# #                         [btn_registrar, btn_buscar_cep, btn_processar_lote],
# #                         alignment=ft.MainAxisAlignment.CENTER,
# #                         spacing=20
# #                     ),
# #
# #                     ft.Divider(height=30),
# #
# #                     ft.Container(
# #                         content=ft.Column([
# #                             ft.Text("Últimos Registros", size=18, weight=ft.FontWeight.BOLD),
# #                             ft.Container(
# #                                 content=lista_registros,
# #                                 height=300,
# #                                 border=ft.border.all(1, ft.Colors.GREY_300),
# #                                 border_radius=10,
# #                                 padding=10
# #                             )
# #                         ]),
# #                         width=600
# #                     )
# #                 ],
# #                 alignment=ft.MainAxisAlignment.CENTER,
# #                 horizontal_alignment=ft.CrossAxisAlignment.CENTER
# #             ),
# #             padding=40
# #         )
# #     )
# #
# #     # Adicionar snackbar à página
# #     page.overlay.append(status_snackbar)
# #
# #     # Carregar registros iniciais
# #     carregar_registros()
# #
# #
# # # Executar a aplicação
# # if __name__ == "__main__":
# #     ft.app(target=main)
#
# import flet as ft
# import mysql.connector
# from datetime import datetime
# import requests
# import base64
# import json
# from typing import Optional
#
#
# # Classe da API dos Correios (mantida do seu código)
# class CorreiosAPI:
#     def __init__(self):
#         self.url_token = "https://api.correios.com.br/token/v1/autentica"
#         self.url_rastreamento = "https://api.correios.com.br/srorastrointerno/v2/rastros"
#         self.auth_header = "Basic NTY3MToxNjU3MTYxMA=="
#         self.token = None
#
#     def get_token(self) -> str:
#         headers = {
#             "Connection": "keep-alive",
#             "Authorization": self.auth_header
#         }
#         try:
#             response = requests.post(self.url_token, headers=headers)
#             response.raise_for_status()
#             data = response.json()
#             self.token = data.get("token")
#             return self.token
#         except Exception as e:
#             print(f"Erro ao obter token: {e}")
#             return None
#
#     def consultar_rastreamento(self, codigo_rastreamento: str) -> Optional[dict]:
#         if not self.token:
#             self.get_token()
#
#         if not self.token:
#             print("Erro: sem token.")
#             return None
#
#         params = {
#             "texto": "I",
#             "resultado": "T",
#             "codigosObjetos": codigo_rastreamento
#         }
#
#         headers = {
#             "Connection": "keep-alive",
#             "Authorization": f"Bearer {self.token}"
#         }
#
#         try:
#             response = requests.get(self.url_rastreamento, params=params, headers=headers)
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             print(f"Erro na consulta ({codigo_rastreamento}): {e}")
#             return None
#
#     def extrair_cep_destinatario(self, dados: dict) -> Optional[str]:
#         try:
#             objetos = dados.get("objetos", [])
#             if not objetos:
#                 return None
#
#             eventos = objetos[0].get("eventos", [])
#             for ev in eventos:
#                 if ev.get("codigo") == "PO":
#                     cep = ev.get("destinatario", {}).get("endereco", {}).get("cep")
#                     return cep
#             return None
#         except:
#             return None
#
#     def get_cep_destinatario(self, codigo: str) -> Optional[str]:
#         print(f"\n🔍 Consultando CEP para {codigo}")
#         dados = self.consultar_rastreamento(codigo)
#         if not dados:
#             return None
#         return self.extrair_cep_destinatario(dados)
#
#
# # Função para conectar ao banco de dados
# def conectar_banco():
#     return mysql.connector.connect(
#         host="10.87.199.29",
#         user="sci_app",
#         password="@sci_app",
#         database="sci"
#     )
#
#
# # Função principal da aplicação Flet
# def main(page: ft.Page):
#     page.title = "Sistema de Registro de Objetos"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.window_width = 800
#     page.window_height = 600
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#
#     # Variáveis globais
#     registros = []
#     api_correios = CorreiosAPI()
#
#     # Componentes da interface
#     titulo = ft.Text(
#         "📦 Sistema de Registro de Objetos",
#         size=28,
#         weight=ft.FontWeight.BOLD,
#         color=ft.Colors.BLUE_800
#     )
#
#     subtitulo = ft.Text(
#         "Bipe o código do objeto para registrar no sistema",
#         size=16,
#         color=ft.Colors.GREY_600
#     )
#
#     # Campo de entrada para código - REMOVIDO autofocus inicial
#     codigo_input = ft.TextField(
#         label="Código do Objeto",
#         hint_text="Digite ou bipe o código de rastreamento",
#         width=400,
#         prefix_icon=ft.Icons.QUEUE_OUTLINED,
#         text_size=16,
#         border_color=ft.Colors.BLUE_400,
#         on_submit=lambda e: registrar_codigo(),
#         on_change=lambda e: auto_registrar(e)  # Nova função para registro automático
#     )
#
#     # Botão de registro
#     btn_registrar = ft.ElevatedButton(
#         text="Registrar Código",
#         icon=ft.Icons.ADD_CIRCLE_OUTLINED,
#         on_click=lambda e: registrar_codigo(),
#         width=200,
#         height=50,
#         style=ft.ButtonStyle(
#             bgcolor=ft.Colors.BLUE_600,
#             color=ft.Colors.WHITE
#         )
#     )
#
#     # Botão para buscar CEP
#     btn_buscar_cep = ft.ElevatedButton(
#         text="Buscar CEP do Último",
#         icon=ft.Icons.SEARCH,
#         on_click=lambda e: buscar_cep_ultimo(),
#         width=200,
#         height=50,
#         style=ft.ButtonStyle(
#             bgcolor=ft.Colors.GREEN_600,
#             color=ft.Colors.WHITE
#         )
#     )
#
#     # Botão para processar lote
#     btn_processar_lote = ft.ElevatedButton(
#         text="Processar Lote",
#         icon=ft.Icons.PLAY_ARROW,
#         on_click=lambda e: processar_lote(),
#         width=200,
#         height=50,
#         style=ft.ButtonStyle(
#             bgcolor=ft.Colors.ORANGE_600,
#             color=ft.Colors.WHITE
#         )
#     )
#
#     # Botão para focar no campo de entrada
#     btn_focar_campo = ft.IconButton(
#         icon=ft.Icons.KEYBOARD,
#         icon_color=ft.Colors.BLUE_600,
#         tooltip="Clique para focar no campo de código",
#         on_click=lambda e: focar_campo_codigo()
#     )
#
#     # Lista de registros
#     lista_registros = ft.ListView(
#         expand=True,
#         spacing=10,
#         padding=20
#     )
#
#     # Mensagem de status
#     status_snackbar = ft.SnackBar(content=ft.Text(""))
#
#     # Função para focar no campo de código
#     def focar_campo_codigo():
#         codigo_input.focus()
#         page.update()
#
#     # Função para registro automático quando o campo muda
#     def auto_registrar(e):
#         # Verifica se o valor tem comprimento típico de código de rastreamento
#         valor = codigo_input.value.strip()
#         if len(valor) >= 13:  # Códigos de rastreamento geralmente têm 13 caracteres
#             registrar_codigo()
#
#     # Função para registrar código no banco
#     def registrar_codigo():
#         codigo = codigo_input.value.strip()
#
#         if not codigo:
#             mostrar_mensagem("❌ Digite um código válido!", ft.Colors.RED)
#             focar_campo_codigo()
#             return
#
#         try:
#             # Conectar ao banco
#             db = conectar_banco()
#             cursor = db.cursor()
#
#             # Verificar se código já existe
#             cursor.execute("SELECT id FROM tb_obj_registrado WHERE codigo = %s", (codigo,))
#             if cursor.fetchone():
#                 mostrar_mensagem("⚠️ Código já registrado!", ft.Colors.ORANGE)
#                 # Limpa o campo e foca novamente
#                 codigo_input.value = ""
#                 focar_campo_codigo()
#                 return
#
#             # Inserir novo registro
#             sql = "INSERT INTO tb_obj_registrado (codigo, data_registro) VALUES (%s, %s)"
#             valores = (codigo, datetime.now())
#             cursor.execute(sql, valores)
#             db.commit()
#
#             # Atualizar lista
#             carregar_registros()
#
#             # Limpar campo e focar novamente
#             codigo_input.value = ""
#             focar_campo_codigo()
#
#             mostrar_mensagem(f"✅ Código {codigo} registrado com sucesso!", ft.Colors.GREEN)
#
#             cursor.close()
#             db.close()
#
#         except Exception as e:
#             mostrar_mensagem(f"❌ Erro ao registrar: {str(e)}", ft.Colors.RED)
#             focar_campo_codigo()
#
#     # Função para buscar CEP do último registro
#     def buscar_cep_ultimo():
#         try:
#             db = conectar_banco()
#             cursor = db.cursor(dictionary=True)
#
#             # Buscar último registro
#             cursor.execute("SELECT codigo FROM tb_obj_registrado ORDER BY id DESC LIMIT 1")
#             ultimo = cursor.fetchone()
#
#             if not ultimo:
#                 mostrar_mensagem("❌ Nenhum registro encontrado!", ft.Colors.RED)
#                 focar_campo_codigo()
#                 return
#
#             codigo = ultimo['codigo']
#             cep = api_correios.get_cep_destinatario(codigo)
#
#             if cep:
#                 resultado = f"{codigo}{cep}"
#                 with open("resultado.txt", "a", encoding="utf-8") as arquivo:
#                     arquivo.write(resultado + "\n")
#                 mostrar_mensagem(f"✅ CEP encontrado: {cep} para {codigo}", ft.Colors.GREEN)
#             else:
#                 mostrar_mensagem(f"❌ CEP não encontrado para {codigo}", ft.Colors.ORANGE)
#
#             cursor.close()
#             db.close()
#             focar_campo_codigo()
#
#         except Exception as e:
#             mostrar_mensagem(f"❌ Erro ao buscar CEP: {str(e)}", ft.Colors.RED)
#             focar_campo_codigo()
#
#     # Função para processar lote
#     def processar_lote():
#         try:
#             db = conectar_banco()
#             cursor = db.cursor(dictionary=True)
#
#             cursor.execute("SELECT id, codigo FROM tb_obj_registrado")
#             registros = cursor.fetchall()
#
#             if not registros:
#                 mostrar_mensagem("❌ Nenhum registro para processar!", ft.Colors.RED)
#                 focar_campo_codigo()
#                 return
#
#             progresso = ft.ProgressBar(width=400, color=ft.Colors.BLUE)
#             progresso_container = ft.Container(
#                 content=progresso,
#                 padding=10
#             )
#
#             page.add(progresso_container)
#             page.update()
#
#             processados = 0
#             total = len(registros)
#
#             for reg in registros:
#                 codigo = reg["codigo"]
#                 cep = api_correios.get_cep_destinatario(codigo)
#
#                 if cep:
#                     resultado = f"{codigo}{cep}"
#                     with open("resultado.txt", "a", encoding="utf-8") as arquivo:
#                         arquivo.write(resultado + "\n")
#                     processados += 1
#
#                 progresso.value = processados / total
#                 page.update()
#
#             page.remove(progresso_container)
#             mostrar_mensagem(f"✅ Processamento concluído! {processados}/{total} objetos", ft.Colors.GREEN)
#
#             cursor.close()
#             db.close()
#             focar_campo_codigo()
#
#         except Exception as e:
#             mostrar_mensagem(f"❌ Erro ao processar lote: {str(e)}", ft.Colors.RED)
#             focar_campo_codigo()
#
#     # Função para carregar registros
#     def carregar_registros():
#         try:
#             lista_registros.controls.clear()
#
#             db = conectar_banco()
#             cursor = db.cursor(dictionary=True)
#
#             cursor.execute("SELECT id, codigo, data_registro FROM tb_obj_registrado ORDER BY id DESC LIMIT 50")
#             registros = cursor.fetchall()
#
#             if not registros:
#                 lista_registros.controls.append(
#                     ft.ListTile(
#                         title=ft.Text("Nenhum registro encontrado"),
#                         leading=ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.GREY)
#                     )
#                 )
#             else:
#                 for reg in registros:
#                     data_formatada = reg['data_registro'].strftime("%d/%m/%Y %H:%M:%S")
#                     lista_registros.controls.append(
#                         ft.Card(
#                             content=ft.Container(
#                                 content=ft.ListTile(
#                                     leading=ft.Icon(ft.Icons.LOCAL_SHIPPING, color=ft.Colors.BLUE),
#                                     title=ft.Text(f"Código: {reg['codigo']}"),
#                                     subtitle=ft.Text(f"ID: {reg['id']} | Data: {data_formatada}"),
#                                     trailing=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
#                                 ),
#                                 padding=10
#                             )
#                         )
#                     )
#
#             cursor.close()
#             db.close()
#             page.update()
#
#         except Exception as e:
#             mostrar_mensagem(f"Erro ao carregar registros: {str(e)}", ft.Colors.RED)
#
#     # Função para mostrar mensagens
#     def mostrar_mensagem(mensagem, cor):
#         status_snackbar.content = ft.Text(mensagem)
#         status_snackbar.bgcolor = cor
#         status_snackbar.open = True
#         page.update()
#
#     # Layout da página
#     page.add(
#         ft.Container(
#             content=ft.Column(
#                 [
#                     ft.Row([titulo], alignment=ft.MainAxisAlignment.CENTER),
#                     ft.Row([subtitulo], alignment=ft.MainAxisAlignment.CENTER),
#
#                     ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
#
#                     ft.Row(
#                         [
#                             codigo_input,
#                             btn_focar_campo
#                         ],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         vertical_alignment=ft.CrossAxisAlignment.CENTER
#                     ),
#
#                     ft.Row(
#                         [btn_registrar, btn_buscar_cep, btn_processar_lote],
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         spacing=20
#                     ),
#
#                     ft.Divider(height=30),
#
#                     ft.Container(
#                         content=ft.Column([
#                             ft.Text("Últimos Registros", size=18, weight=ft.FontWeight.BOLD),
#                             ft.Container(
#                                 content=lista_registros,
#                                 height=300,
#                                 border=ft.border.all(1, ft.Colors.GREY_300),
#                                 border_radius=10,
#                                 padding=10
#                             )
#                         ]),
#                         width=600
#                     )
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER
#             ),
#             padding=40
#         )
#     )
#
#     # Adicionar snackbar à página
#     page.overlay.append(status_snackbar)
#
#     # Carregar registros iniciais
#     carregar_registros()
#
#     # Focar no campo de código após carregar tudo
#     page.update()
#     focar_campo_codigo()
#
#
# # Executar a aplicação
# if __name__ == "__main__":
#     ft.app(target=main)
import flet as ft
from datetime import datetime
import requests
import sqlite3
import os
from typing import Optional


# Classe da API dos Correios (mantida do seu código)
class CorreiosAPI:
    def __init__(self):
        self.url_token = "https://api.correios.com.br/token/v1/autentica"
        self.url_rastreamento = "https://api.correios.com.br/srorastrointerno/v2/rastros"
        self.auth_header = "Basic NTY3MToxNjU3MTYxMA=="
        self.token = None

    def get_token(self) -> str:
        headers = {
            "Connection": "keep-alive",
            "Authorization": self.auth_header
        }
        try:
            response = requests.post(self.url_token, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.token = data.get("token")
            return self.token
        except Exception as e:
            print(f"Erro ao obter token: {e}")
            return None

    def consultar_rastreamento(self, codigo_rastreamento: str) -> Optional[dict]:
        if not self.token:
            self.get_token()

        if not self.token:
            print("Erro: sem token.")
            return None

        params = {
            "texto": "I",
            "resultado": "T",
            "codigosObjetos": codigo_rastreamento
        }

        headers = {
            "Connection": "keep-alive",
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.get(self.url_rastreamento, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro na consulta ({codigo_rastreamento}): {e}")
            return None

    def extrair_cep_destinatario(self, dados: dict) -> Optional[str]:
        try:
            objetos = dados.get("objetos", [])
            if not objetos:
                return None

            eventos = objetos[0].get("eventos", [])
            for ev in eventos:
                if ev.get("codigo") == "PO":
                    cep = ev.get("destinatario", {}).get("endereco", {}).get("cep")
                    return cep
            return None
        except:
            return None

    def get_cep_destinatario(self, codigo: str) -> Optional[str]:
        print(f"\n🔍 Consultando CEP para {codigo}")
        dados = self.consultar_rastreamento(codigo)
        if not dados:
            return None
        return self.extrair_cep_destinatario(dados)


# Função para conectar ao banco de dados SQLite
def conectar_banco():
    # Cria o banco de dados na mesma pasta do script
    db_path = "registro_objetos.db"

    # Conectar ao banco (cria se não existir)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome

    # Criar tabela se não existir
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_obj_registrado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            data_registro TEXT NOT NULL,
            cep TEXT,
            status TEXT DEFAULT 'pendente'
        )
    ''')

    # Criar índice para melhor performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_codigo 
        ON tb_obj_registrado(codigo)
    ''')

    conn.commit()
    return conn


# Função para inicializar o banco de dados
def inicializar_banco():
    conn = conectar_banco()
    conn.close()


# Função principal da aplicação Flet
def main(page: ft.Page):
    page.title = "Sistema de Registro de Objetos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.full_screen = True
    #page.window_width = 800
    #page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Variáveis globais
    api_correios = CorreiosAPI()

    # Componentes da interface
    titulo = ft.Text(
        "📦 Sistema de Registro de Objetos",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_800
    )

    subtitulo = ft.Text(
        "Bipe o código do objeto para registrar no sistema",
        size=16,
        color=ft.colors.GREY_600
    )

    # Campo de entrada para código
    codigo_input = ft.TextField(
        label="Código do Objeto",
        hint_text="Digite ou bipe o código de rastreamento",
        width=400,
        prefix_icon=ft.icons.QUEUE_OUTLINED,
        text_size=16,
        border_color=ft.colors.BLUE_400,
        on_submit=lambda e: registrar_codigo(),
        on_change=lambda e: auto_registrar(e)
    )

    # Botão de registro
    btn_registrar = ft.ElevatedButton(
        text="Registrar Código",
        icon=ft.icons.ADD_CIRCLE_OUTLINED,
        on_click=lambda e: registrar_codigo(),
        width=200,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE
        )
    )
    btn_sair = ft.ElevatedButton(
        text="Sair",
        icon=ft.icons.CLOSE,
        width=200,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.RED_600,
            color=ft.colors.WHITE
        ),
        on_click=lambda e: page.window.close()

    )

    # Botão para buscar CEP
    btn_buscar_cep = ft.ElevatedButton(
        text="Buscar CEP do Último",
        icon=ft.icons.SEARCH,
        on_click=lambda e: buscar_cep_ultimo(),
        width=200,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE
        )
    )

    # Botão para processar lote
    btn_processar_lote = ft.ElevatedButton(
        text="Processar Lote",
        icon=ft.icons.PLAY_ARROW,
        on_click=lambda e: processar_lote(),
        width=200,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.ORANGE_600,
            color=ft.colors.WHITE
        )
    )

    # Botão para focar no campo de entrada
    btn_focar_campo = ft.IconButton(
        icon=ft.icons.KEYBOARD,
        icon_color=ft.colors.BLUE_600,
        tooltip="Clique para focar no campo de código",
        on_click=lambda e: focar_campo_codigo()
    )


    # Botão para limpar banco (opcional, para testes)
    # btn_limpar = ft.ElevatedButton(
    #     text="Limpar Registros",
    #     icon=ft.Icons.DELETE_OUTLINE,
    #     on_click=lambda e: limpar_registros(),
    #     width=200,
    #     height=50,
    #     style=ft.ButtonStyle(
    #         bgcolor=ft.Colors.RED_600,
    #         color=ft.Colors.WHITE
    #     )
    # )

    # Lista de registros
    lista_registros = ft.ListView(
        expand=True,
        spacing=10,
        padding=20
    )

    # Contador de registros
    contador_registros = ft.Text("0 registros", size=14, color=ft.colors.GREY_600)

    # Mensagem de status
    status_snackbar = ft.SnackBar(content=ft.Text(""))

    # Função para focar no campo de código
    def focar_campo_codigo():
        codigo_input.focus()
        page.update()

    # Função para registro automático quando o campo muda
    def auto_registrar(e):
        valor = codigo_input.value.strip()
        # Verifica se o valor tem comprimento típico de código de rastreamento (13 caracteres)
        if len(valor) == 13:
            registrar_codigo()

    # Função para registrar código no banco
    def registrar_codigo():
        codigo = codigo_input.value.strip()

        if not codigo:
            #mostrar_mensagem("❌ Digite um código válido!", ft.colors.RED)
            focar_campo_codigo()
            return

        try:
            # Conectar ao banco
            conn = conectar_banco()
            cursor = conn.cursor()

            # Verificar se código já existe
            cursor.execute("SELECT id FROM tb_obj_registrado WHERE codigo = ?", (codigo,))
            if cursor.fetchone():
                #mostrar_mensagem("⚠️ Código já registrado!", ft.Colors.ORANGE)
                codigo_input.value = ""
                focar_campo_codigo()
                return

            # Inserir novo registro
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO tb_obj_registrado (codigo, data_registro) VALUES (?, ?)",
                (codigo, data_atual)
            )
            conn.commit()

            # Atualizar lista e contador
            carregar_registros()
            atualizar_contador()

            # Limpar campo e focar novamente
            codigo_input.value = ""
            focar_campo_codigo()

            #mostrar_mensagem(f"✅ Código {codigo} registrado com sucesso!", ft.colors.GREEN)

            cursor.close()
            conn.close()

        except Exception as e:
            #mostrar_mensagem(f"❌ Erro ao registrar: {str(e)}", ft.colors.RED)
            focar_campo_codigo()

    # Função para buscar CEP do último registro
    def buscar_cep_ultimo():
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Buscar último registro
            cursor.execute("SELECT codigo FROM tb_obj_registrado ORDER BY id DESC LIMIT 1")
            ultimo = cursor.fetchone()

            if not ultimo:
                mostrar_mensagem("❌ Nenhum registro encontrado!", ft.colors.RED)
                focar_campo_codigo()
                return

            codigo = ultimo[0]  # Acessar por índice
            cep = api_correios.get_cep_destinatario(codigo)

            if cep:
                resultado = f"{codigo}|{cep}"
                with open("resultado.txt", "a", encoding="utf-8") as arquivo:
                    arquivo.write(resultado + "\n")

                # Atualizar o registro no banco com o CEP encontrado
                cursor.execute(
                    "UPDATE tb_obj_registrado SET cep = ?, status = 'processado' WHERE codigo = ?",
                    (cep, codigo)
                )
                conn.commit()

                #mostrar_mensagem(f"✅ CEP encontrado: {cep} para {codigo}", ft.colors.GREEN)
                carregar_registros()  # Atualizar a lista para mostrar o CEP
            else:
                mostrar_mensagem(f"❌ CEP não encontrado para {codigo}", ft.colors.ORANGE)

            cursor.close()
            conn.close()
            focar_campo_codigo()

        except Exception as e:
            #mostrar_mensagem(f"❌ Erro ao buscar CEP: {str(e)}", ft.colors.RED)
            focar_campo_codigo()

    # Função para processar lote
    # def processar_lote():
    #     try:
    #         conn = conectar_banco()
    #         cursor = conn.cursor()
    #
    #         cursor.execute("SELECT id, codigo FROM tb_obj_registrado WHERE cep IS NULL")
    #         registros = cursor.fetchall()
    #
    #         if not registros:
    #             mostrar_mensagem("✅ Todos os registros já foram processados!", ft.colors.GREEN)
    #             focar_campo_codigo()
    #             return
    #
    #         progresso = ft.ProgressBar(width=400, color=ft.colors.BLUE)
    #         progresso_container = ft.Container(
    #             content=progresso,
    #             padding=10
    #         )
    #
    #         page.add(progresso_container)
    #         page.update()
    #
    #         processados = 0
    #         total = len(registros)
    #
    #         for reg in registros:
    #             codigo = reg[1]  # Índice 1 é o código
    #             cep = api_correios.get_cep_destinatario(codigo)
    #
    #             if cep:
    #                 resultado = f"{codigo}|{cep}"
    #                 with open("resultado.txt", "a", encoding="utf-8") as arquivo:
    #                     arquivo.write(resultado + "\n")
    #
    #                 # Atualizar no banco
    #                 cursor.execute(
    #                     "UPDATE tb_obj_registrado SET cep = ?, status = 'processado' WHERE id = ?",
    #                     (cep, reg[0])
    #                 )
    #                 conn.commit()
    #
    #                 processados += 1
    #
    #             progresso.value = processados / total
    #             page.update()
    #
    #         page.remove(progresso_container)
    #         mostrar_mensagem(f"✅ Processamento concluído! {processados}/{total} objetos", ft.colors.GREEN)
    #
    #         cursor.execute("DELETE FROM tb_obj_registrado WHERE cep IS NOT NULL")
    #         conn.commit()
    #
    #         # Atualizar lista
    #         carregar_registros()
    #
    #         cursor.close()
    #         conn.close()
    #         focar_campo_codigo()
    #
    #     except Exception as e:
    #         mostrar_mensagem(f"❌ Erro ao processar lote: {str(e)}", ft.colors.RED)
    #         focar_campo_codigo()

    # Função para carregar registros

    def processar_lote():
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            while True:

                # Buscar apenas 50 registros por vez
                cursor.execute(
                    "SELECT id, codigo FROM tb_obj_registrado WHERE cep IS NULL LIMIT 50"
                )
                registros = cursor.fetchall()

                # Se acabou, encerra
                if not registros:
                    mostrar_mensagem("✅ Todos os registros já foram processados!", ft.colors.GREEN)
                    focar_campo_codigo()
                    break

                # Barra de progresso
                progresso = ft.ProgressBar(width=400, color=ft.colors.BLUE)
                progresso_container = ft.Container(content=progresso, padding=10)

                page.add(progresso_container)
                page.update()

                processados = 0
                total = len(registros)

                # Processa cada item do lote
                for reg in registros:
                    codigo = reg[1]

                    try:
                        cep = api_correios.get_cep_destinatario(codigo)
                    except Exception as erro_api:
                        cep = None

                    if cep:
                        # CEP encontrado – processa normalmente
                        resultado = f"{codigo}|{cep}"
                        with open("resultado.txt", "a", encoding="utf-8") as arquivo:
                            arquivo.write(resultado + "\n")

                        cursor.execute(
                            "UPDATE tb_obj_registrado SET cep = ?, status = 'processado' WHERE id = ?",
                            (cep, reg[0])
                        )
                    else:
                        # CEP não encontrado / erro na API → MARCAR COMO ERRO
                        cursor.execute(
                            "UPDATE tb_obj_registrado SET cep = 'ERRO', status = 'erro' WHERE id = ?",
                            (reg[0],)
                        )

                    conn.commit()

                    processados += 1
                    progresso.value = processados / total
                    page.update()

                # Remove barra de progresso
                page.remove(progresso_container)
                mostrar_mensagem(
                    f"✅ Lote concluído! {processados}/{total} objetos",
                    ft.colors.GREEN
                )
                page.update()

                # Mantive sua lógica: apaga os processados (inclui 'ERRO')
                cursor.execute("DELETE FROM tb_obj_registrado WHERE cep IS NOT NULL")
                conn.commit()

                # Atualiza a lista visível
                carregar_registros()

            cursor.close()
            conn.close()
            focar_campo_codigo()

        except Exception as e:
            mostrar_mensagem(f"❌ Erro ao processar lote: {str(e)}", ft.colors.RED)
            focar_campo_codigo()

    def carregar_registros():
        try:
            lista_registros.controls.clear()

            conn = conectar_banco()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, codigo, data_registro, cep FROM tb_obj_registrado ORDER BY id DESC LIMIT 50"
            )
            registros = cursor.fetchall()

            if not registros:
                lista_registros.controls.append(
                    ft.ListTile(
                        title=ft.Text("Nenhum registro encontrado"),
                        leading=ft.Icon(ft.icons.INFO_OUTLINE, color=ft.colors.GREY)
                    )
                )
            else:
                for reg in registros:
                    # Formatar data
                    data_original = reg[2]
                    try:
                        data_obj = datetime.strptime(data_original, "%Y-%m-%d %H:%M:%S")
                        data_formatada = data_obj.strftime("%d/%m/%Y %H:%M:%S")
                    except:
                        data_formatada = data_original

                    # Definir cor baseada no CEP
                    cep = reg[3]
                    cor_icone = ft.colors.GREEN if cep else ft.colors.BLUE

                    lista_registros.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.LOCAL_SHIPPING, color=cor_icone),
                                    title=ft.Text(f"Código: {reg[1]}"),
                                    subtitle=ft.Text(
                                        f"ID: {reg[0]} | Data: {data_formatada}\n"
                                        f"CEP: {cep if cep else 'Não processado'}"
                                    ),
                                    trailing=ft.Icon(
                                        ft.icons.CHECK_CIRCLE if cep else ft.icons.PENDING,
                                        color=cor_icone
                                    )
                                ),
                                padding=10
                            )
                        )
                    )

            cursor.close()
            conn.close()
            page.update()

        except Exception as e:
            mostrar_mensagem(f"Erro ao carregar registros: {str(e)}", ft.colors.RED)

    # Função para atualizar contador
    def atualizar_contador():
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Total de registros
            cursor.execute("SELECT COUNT(*) FROM tb_obj_registrado")
            total = cursor.fetchone()[0]

            # Registros processados
            cursor.execute("SELECT COUNT(*) FROM tb_obj_registrado WHERE cep IS NOT NULL")
            processados = cursor.fetchone()[0]

            contador_registros.value = f"{total} registros ({processados} com CEP)"

            cursor.close()
            conn.close()
            page.update()

        except Exception as e:
            print(f"Erro ao atualizar contador: {e}")



    # Função para limpar registros (opcional)
    # def limpar_registros():
    #     def confirmar_limpeza(e):
    #         try:
    #             conn = conectar_banco()
    #             cursor = conn.cursor()
    #
    #             cursor.execute("DELETE FROM tb_obj_registrado")
    #             conn.commit()
    #
    #             cursor.close()
    #             conn.close()
    #
    #             carregar_registros()
    #             atualizar_contador()
    #             mostrar_mensagem("✅ Todos os registros foram removidos!", ft.Colors.GREEN)
    #
    #         except Exception as e:
    #             mostrar_mensagem(f"❌ Erro ao limpar: {str(e)}", ft.Colors.RED)
    #
    #         page.dialog.open = False
    #         page.update()
    #
    #     # Diálogo de confirmação
    #     dlg = ft.AlertDialog(
    #         title=ft.Text("Confirmar Limpeza"),
    #         content=ft.Text("Tem certeza que deseja remover TODOS os registros?\nEsta ação não pode ser desfeita."),
    #         actions=[
    #             ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg, 'open', False) or page.update()),
    #             ft.TextButton("Confirmar", on_click=confirmar_limpeza, style=ft.ButtonStyle(color=ft.Colors.RED)),
    #         ],
    #     )
    #
    #     page.dialog = dlg
    #     dlg.open = True
    #     page.update()

    # Função para mostrar mensagens
    def mostrar_mensagem(mensagem, cor):
        status_snackbar.content = ft.Text(mensagem)
        status_snackbar.bgcolor = cor
        status_snackbar.open = True
        page.update()

    # Layout da página
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row([titulo], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([subtitulo], alignment=ft.MainAxisAlignment.CENTER),

                    ft.Row(
                        [contador_registros],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),

                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),

                    ft.Row(
                        [
                            codigo_input,
                            btn_focar_campo
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),

                    ft.Row(
                        [btn_registrar, btn_buscar_cep, btn_processar_lote,btn_sair],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    ),

                    # ft.Row(
                    #     [btn_exportar, btn_limpar],
                    #     alignment=ft.MainAxisAlignment.CENTER,
                    #     spacing=20
                    # ),

                    ft.Divider(height=30),

                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Últimos Registros", size=18, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.icons.REFRESH,
                                    icon_color=ft.colors.BLUE,
                                    tooltip="Atualizar lista",
                                    on_click=lambda e: (carregar_registros(), atualizar_contador())
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(
                                content=lista_registros,
                                height=300,
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=10,
                                padding=10
                            )
                        ]),
                        width=600
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=40
        )
    )

    # Adicionar snackbar à página
    page.overlay.append(status_snackbar)

    # Inicializar banco e carregar dados
    inicializar_banco()
    carregar_registros()
    atualizar_contador()

    # Focar no campo de código após carregar tudo
    page.update()
    focar_campo_codigo()


# Executar a aplicação
if __name__ == "__main__":
    ft.app(target=main)