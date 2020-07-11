#discord.py
import discord
from discord.ext import commands,tasks
#requests
import requests
#pillow
from PIL import Image

#native python
from itertools import cycle
from io import BytesIO
import random
import os
import time

def get_token(): 
	with open('res/key.txt','r') as file:
		return file.readline()

token = get_token()

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

#variaveis para controle de spam
usuarios = []
#pode ser exploitado, porém caso queiram exploitar o bot ao fazê-lo spammar o chat, os
#próprios usuários estão spammando o chat, então não faz sentido fazer um sistema robusto
#para esse tipo de coisa :p
ultimo_usuario=0
#contador dos tops para a não repetição de imagens (até o final do vetor de imagens)
tops=0

#o total de imagens de "top" dentro da pasta de imagens do bot
imagens_top=0
for filename in os.listdir('res/imgs/ok'):
	imagens_top+=1

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game('.help Para Comandos!'))
	print('Bot is ready.')

@client.event
async def on_member_join(member):
	print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
	print(f'{member} has left the server')

@client.event
async def on_command_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Tem pelo menos um argumento Faltando!')

#----------------------------------------------COMANDOS DE TEXTO----------------------------------------------
@client.command()
async def ping(ctx):
	if await usuario_spam(ctx):
		return
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def help(ctx):
	if await usuario_spam(ctx):
		return
	await ctx.send('```Null\n.help ---> Você está aqui!\n.ping - Mostra o seu ping (USA)\n.8ball - Faça uma pergunta à bola oito\n\tTambém serve: ._8ball - .bola8\n.roll - Role um dado\n\tUsos: .roll 2d20 - 5 // .roll 20\n.ship - Shippe duas pessoas e veja se rola algo!\n.caracoroa - Jogue cara ou coroa!\n\tTambém serve: .coinflip - .caracoroa\n.cancela - Marque alguém e CANCELE a pessoa!!!\n.ok - Uma foto aleatória de um ok/top\n\tTambém serve: .top\n.mario - mario_tpose_praia.png\n.foto_perfil - Mostra a foto de perfil da pessoa marcada\n.bafora - Selo do "Bafora e Passa" na última foto mandada\n.monstro - "Um monstro desses merece perdão?" na última foto mandada\n.bolsonaro - Faça o bolsonaro apontar para última foto mandada```')

@client.command(aliases=['8ball','bola8'])
async def _8ball(ctx, * ,question=''):
	if await usuario_spam(ctx):
		return
	responses = [	'Sim',
					'Não',
					'As estrelas dizem que não',
					'Sem sombra de dúvida',
					'A resposta não é certa, pergunte mais tarde',
					'E assim será',
					'Não aposte nisso',
					'Indicações dizem que sim',
					'Foque e pergunte novamente',
					'As estrelas dizem que não',
					'Improvável',
					'As chances não são boas',
					'Parece que sim',
					'Me consulte mais tarde',
					'Absolutamente',
					'Positivo!',
					'Não consigo prever agora',
					'Aparenta ser um "Sim"',
					'Bem provável',
					'Você pode contar com isso',
					'Não consigo dizer agora',
				]
	if (question==''):
		#potencial pra easter egg ou somente uma mensagem pra usuario burro?
		await ctx.send('Tenho cara de vidente? Faz uma perguta que daí eu respondo')
	else:			
		await ctx.send(f'{random.choice(responses)}')

@client.command()
async def roll(ctx, numero,sinal='',mod='0'):
	if await usuario_spam(ctx):
		return
	#Para dados únicos
	if numero.isnumeric() or numero[:1] == 'd':
		if numero[:1] == 'd':
			if int(numero[1:]) > 1001:
				await ctx.send(f'Número alto demais! {ctx.message.author.mention}')
				return
			dadinho = random.randint(1,int(numero[1:]))
			rodado = numero[1:]
		else:
			if int(numero) > 1001:
				await ctx.send(f'Número alto demais! {ctx.message.author.mention}')
				return
			dadinho = random.randint(1,int(numero))
			rodado = numero
		if sinal == '+':
			if not mod.isnumeric():
				await ctx.send(f'"{mod}" não é um número válido! {ctx.message.author.mention}')
			await ctx.send(f'{ctx.message.author.mention} rolou **{rodado}**... e conseguiu **{dadinho + int(mod)}**!\n ``{dadinho + int(mod)}`` » {dadinho} = {dadinho} ``+ {mod} = {dadinho + int(mod)}``')
		elif sinal == '-':
			if not mod.isnumeric():
				await ctx.send(f'"{mod}" não é um número válido! {ctx.message.author.mention}')
			await ctx.send(f'{ctx.message.author.mention} rolou **{rodado}**... e conseguiu **{dadinho - int(mod)}**!\n ``{dadinho - int(mod)}`` » {dadinho} = {dadinho} ``- {mod} = {dadinho - int(mod)}``')
		else:
			await ctx.send(f'{ctx.message.author.mention} rolou **{rodado}**... e conseguiu **{dadinho}**!')
	#Para múltiplos dados
	elif numero[:1].isnumeric() and  numero[-1:].isnumeric():
		total_dados_rolados,dado = numero.split('d')
		valor_somado_dados = 0
		if total_dados_rolados.isnumeric() and dado.isnumeric():
			if int(total_dados_rolados) > 100 or int(dado) > 1001:
				await ctx.send(f'Número alto demais! {ctx.message.author.mention}')
				return
			dados_rolados = []
			for i in range(int(total_dados_rolados)):
				dadinho = random.randint(1,int(dado))
				dados_rolados.append(dadinho)
				valor_somado_dados+= dadinho
			string_todos_dados_rolados = (' + '.join(str(d) for d in dados_rolados))
			if sinal == '+':
				if not mod.isnumeric():
					await ctx.send(f'"{mod}" não é um número válido! {ctx.message.author.mention}')
				await ctx.send(f'{ctx.message.author.mention} rolou **{dado}**... e conseguiu **{valor_somado_dados + mod}**!\n``{valor_somado_dados + mod}`` » {string_todos_dados_rolados} = {valor_somado_dados}  ``+ {mod} = {valor_somado_dados + mod}``')
			elif sinal == '-':
				if not mod.isnumeric():
					await ctx.send(f'"{mod}" não é um número válido! {ctx.message.author.mention}')
				await ctx.send(f'{ctx.message.author.mention} rolou **{dado}**... e conseguiu **{valor_somado_dados - mod}**!\n``{valor_somado_dados - mod}`` » {string_todos_dados_rolados} = {valor_somado_dados}  ``- {mod} = {valor_somado_dados - mod}``')
			else:
				await ctx.send(f'{ctx.message.author.mention} rolou **{dado}**... e conseguiu **{valor_somado_dados}**!\n``{valor_somado_dados}`` » {string_todos_dados_rolados}')

@client.command()
async def ship(ctx, member1: discord.Member, member2: discord.Member):
	if await usuario_spam(ctx):
		return
	if member1.id == member2.id:
		await ctx.send('Amor próprio é excelente, porém não funciona aqui!')
		return
	shipPercent= (int(member1.discriminator) + int(member2.discriminator)) % 100

	if shipPercent < 20:
		string = 'Olha... Talvez seja melhor vocês tentarem com outra pessoa'
	elif shipPercent <= 40:
		string = 'Talvez algo de bom possa acontecer entre vocês!'
	elif shipPercent <= 60:
		string = 'A chance é maior do que a de muitos casais!'
	elif shipPercent <= 80:
		string = 'Olha, vocês são um casal incrível, que sincronia sensacional!'
	else:
		string = 'Vocês nasceram um pro outro... essa é a primeira vez que vejo tamanha sincronia e amor em um só casal!'

	string_final = string + f'\n{member1.mention} & {member2.mention}'
	if member1.id > member2.id:
		await cria_foto_ship(ctx,member1,member2,shipPercent,string_final)
	else:
		await cria_foto_ship(ctx,member2,member1,shipPercent,string_final)
	await ctx.send(f'``{shipPercent}%``, {string_final}\n', file=discord.File(f'temp/{id_foto}.png'))


@client.command(aliases=['coinflip','caraoucoroa'])
async def caracoroa(ctx):
	if await usuario_spam(ctx):
		return
	if random.randint(1,2) == 1:
		await ctx.send(f'Cara!')
	else:
		await ctx.send(f'Coroa!')

@client.command(aliases=['cancelado','cancelada','cancelar'])
async def cancela(ctx, member : discord.Member):
	if await usuario_spam(ctx):
		return
	await ctx.send(f'{member.mention} Acaba de ser cancelado(a)')

#----------------------------------------------COMANDOS DE FOTOS----------------------------------------------
@client.command(aliases=['ok'])
async def top(ctx):
	global tops
	global imagens_top
	if await usuario_spam(ctx):
		return
	if tops > imagens_top:
		tops=1
	else:
		tops+=1
	await ctx.send(file=discord.File(f'res/imgs/ok/{tops}.png'))

@client.command()
async def mario(ctx):
	if await usuario_spam(ctx):
		return
	await ctx.send("It's-a me! Mario!",file=discord.File('res/imgs/mario/mario_tpose_praia.png'))

@client.command()
async def foto_perfil(ctx, member: discord.Member):
	if await usuario_spam(ctx):
		return
	im = await returns_user_photo_in_bytes(ctx,member)
	await ctx.send(file=discord.File(im,'foto.png'))

@client.command()
async def bafora(ctx):
	if await usuario_spam(ctx):
		return
	foto1 = await returns_latest_image_in_bytes(ctx)
	foto2 = await watermark_with_transparency(ctx,'res/imgs/bafora_e_passa/bafora_e_passa_logo.png',foto1,'bafora')

@client.command()
async def monstro(ctx):
	if await usuario_spam(ctx):
		return
	foto1 = await returns_latest_image_in_bytes(ctx)
	await watermark_with_transparency(ctx,'res/imgs/monstro_merece_perdao/monstro_merece_perdao.png',foto1,'monstro')

@client.command()
async def bolsonaro(ctx):
	if await usuario_spam(ctx):
		return
	foto1 = await returns_latest_image_in_bytes(ctx)
	await bolsonaro(ctx,foto1)

#	----------------------------------------------FUNCOES----------------------------------------------
async def usuario_spam(ctx):
	#variavel global fodase
	global usuarios
	global ultimo_usuario
	flag=False
	timestamp = int(time.time())
	for i,linha in enumerate(usuarios):
		x,y = linha
		if x == ctx.message.author.id:
			if y+3 > timestamp:
				usuarios[i] = (x,timestamp)
				if ultimo_usuario != ctx.message.author.id:
					await ctx.send(f'Espere mais um pouco para enviar mensagens! {ctx.message.author.mention}')
					ultimo_usuario = ctx.message.author.id
					return True
				return True
			else:
				usuarios[i] = (x,timestamp)
				ultimo_usuario = 0
				return False
	tupple = [ctx.message.author.id,timestamp]
	usuarios.append(tupple)
	ultimo_usuario = 0
	return False

async def cria_foto_ship(ctx, member : discord.Member, member2 : discord.Member,shipPercent,string_final):
	foto_m1 = await returns_user_photo_in_bytes(ctx, member)
	foto_m2 = await returns_user_photo_in_bytes(ctx, member2)

	id_foto = member2.id + member.id
	foto1 = Image.open(foto_m1)
	foto2 = Image.open(foto_m2)
	foto3 = Image.open(f'res/imgs/heart/heart.png')
	tamanho = (128,128)
	foto1_r = foto1.resize(tamanho)
	foto2_r = foto2.resize(tamanho)
	transparent = Image.new('RGBA', (388, 128), (0,0,0,0))
	transparent.paste(foto1_r, (0,0))
	transparent.paste(foto3,(130,0))
	transparent.paste(foto2_r, (260,0))

	#obrigado stack overflow :bless:
	imgByteArr = BytesIO()
	transparent.save(imgByteArr, format='PNG')
	imgByteArr = imgByteArr.getvalue()

	await ctx.send(f'``{shipPercent}%``, {string_final}',file=discord.File(BytesIO(imgByteArr),'foto.png'))

async def returns_user_photo_in_bytes(ctx, member : discord.Member):
	r = requests.get(member.avatar_url)
	return BytesIO(r.content)

async def returns_latest_image_in_bytes(ctx):
	async for message in ctx.history(limit=40):	
		try:
			pic_ext = ['.jpg','.png','.jpeg','.webp']
			for ext in pic_ext:
				if message.attachments[0].filename.endswith(ext):
					if message.attachments[0].size > 1536000:
						await ctx.send('A foto mandada é grande demais! (Limite de 1.5MB)')
						return
					else:
						r = requests.get(message.attachments[0].proxy_url)
						return BytesIO(r.content)
		except IndexError:
			pass
		
async def watermark_with_transparency(ctx,watermark_image_path,imagem,nome):
	base_image = Image.open(imagem)
	watermark_original = Image.open(watermark_image_path)

	width, height = base_image.size
	width_transp, height_transp = watermark_original.size

	if nome == 'monstro':
		resize_mult = width/width_transp
		watermark = watermark_original.resize((int(width_transp*resize_mult),int(height_transp*resize_mult)) )
		width_mons_resiz,height_mons_resiz = watermark.size
	if nome == 'bafora':
		resize_mult = (width/width_transp) / 2
		watermark = watermark_original.resize((int(width_transp*resize_mult), int(height_transp*resize_mult)) )
		width_transp, height_transp = watermark.size
	
	transparent = Image.new('RGBA', (width, height), (0,0,0,0))
	transparent.paste(base_image, (0,0))
	
	if nome == 'bafora':
		x,y = [round(width/2)-round(width_transp/2),round(height/10)]
	elif nome == 'monstro':
		x,y = [0,height - height_mons_resiz]

	transparent.paste(watermark, (x,y), mask=watermark)
	
	#obrigado stack overflow :bless:
	imgByteArr = BytesIO()
	transparent.save(imgByteArr, format='PNG')
	imgByteArr = imgByteArr.getvalue()

	await ctx.send(file=discord.File(BytesIO(imgByteArr),'foto.png'))

async def bolsonaro(ctx,foto_orig):
	file_name = ctx.message.channel.id
	bonoro = Image.open('res/imgs/bolsonaro/bolsonaro.png')
	img_ori = Image.open(foto_orig)

	width_ori,height_ori = img_ori.size
	width_bols,height_bols = bonoro.size

	resize_mult_w = 661 / width_ori
	resize_mult_h = 360 / height_ori
	foto_ori_resized = img_ori.resize((int(resize_mult_w*width_ori),int(resize_mult_h*height_ori)) )

	transparent = Image.new('RGBA', bonoro.size, (0,0,0,0))
	transparent.paste(foto_ori_resized,(255,28))

	transparent.paste(bonoro,(0,0),mask=bonoro)

	#obrigado stack overflow :bless:
	imgByteArr = BytesIO()
	transparent.save(imgByteArr, format='PNG')
	imgByteArr = imgByteArr.getvalue()

	await ctx.send(file=discord.File(BytesIO(imgByteArr),'foto.png'))


#COMANDOS PERIGOSOS!
"""
@client.command()
async def clear(ctx, ammount=5):
	await ctx.channel.purge(limit=ammount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'Kicked {member.mention}')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if(user.name, user.discriminator) == (member_name,member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')
			return
"""

client.run(f'{token}')