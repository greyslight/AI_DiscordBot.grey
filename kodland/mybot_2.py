import discord
from discord.ext import commands
from mycode import gen_pass
import random, os
import time
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)




@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def laugh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def generatepass(ctx):
    await ctx.send("Berapa panjang passwordnya?")
    panjang = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if panjang.content.isdigit():
        panjang = int(panjang.content)
        await ctx.send(f"Ini passwordnya: {gen_pass(panjang)}")
    else:
        await ctx.send("Eror, ulang lagi. Coba masukkan menggunakan angka(1,3,5...)")


@bot.command()
async def pangkatkan(ctx):
    await ctx.send("angka apa yang anda ingin pangkatkan?")
    angka = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel) #input() versi discord bot
    if angka.content.isdigit(): #isdigit() untuk cek string adalah sebauh interger, isalpha() untuk mengecek string adalah sebuah string
        angka = int(angka.content) #bisa membaca isi dari apa yang kita tulis di chat
        await ctx.send(f'Berikut pangkat dari {angka}')
        await ctx.send(angka**2)
    else:
        await ctx.send("Eror, ulang lagi. Coba masukkan menggunakan angka(1,3,5...)")

@bot.command()
async def soalmtk(ctx):
    a = random.randint(1, 30)
    b = random.randint(1, 30)
    list_hitung = ["+", "-", "x"]
    operator = random.choice(list_hitung)
    print(operator)

    correctRes = 0
    if operator == "+":
        correctRes = a + b
    elif operator == "-":
        if a < b:
            a = b + random.randint(2,10)
        correctRes = a - b
    elif operator == "x":
        correctRes = a*b
    await ctx.send(f"berapa {a} {operator} {b}?")

    tebak = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if tebak.content.isdigit():
        tebak = int(tebak.content)
        if tebak == correctRes:
            await ctx.send("Kamu benar!")
        else:
            await ctx.send(f"Maaf kamu salah, jawaban dari {a} {operator} {b} adalah {correctRes}") #f"string" untuk bisa menambahkan variable dengan {var}
    else:
        await ctx.send("Eror, ulang lagi. Coba masukkan menggunakan angka(1,3,5...)")


@bot.command()
async def guess(ctx):
    await ctx.send("tebak angka dari 1 sampai 10")
    jawaban = random.randint(1,10)
    tebak = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    tebak = int(tebak.content)
 
    if tebak == jawaban:
        await ctx.send("Kamu benar!")
    else:
        await ctx.send(f"Maaf kamu salah, jawabannya {jawaban}")


@bot.command()
async def meme(ctx):
    folder = os.listdir("gambar_meme")
    randomImg = random.choice(folder)
    directory = f'gambar_meme/{randomImg}'
    with open(directory, "rb") as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def animal(ctx):
    folder = os.listdir("meme_binatang")
    randomImg = random.choice(folder)
    directory = f'meme_binatang/{randomImg}'
    with open(directory, "rb") as f:
        picture = discord.File(f)
    await ctx.send(file=picture)


@bot.command()
async def showcommands(ctx):
    await ctx.send("Ini semua command dari bot ini:")
    list_command = [
        "$hello : menyapa bot",
        "$laugh(optional pakai angka): membuat bot tertawa",
        "$generatepass(dengan angka untuk panjang password) : mengenerate password random",
        "$pangkatkan(dengan angka) : mempangkat 2 sebuah angka",
        "$guess : bermain tebak angka dengan bot",
        "$soalmtk : bot memberikan soal matematika tentang penjumlahan dan pengurangan",
        "$meme : bot mengunggah sebuah meme random",
        "$animal : bot mengunggah sebuah meme binatang lucu secara random",
        "$birdspot(gambar) : bot mengidentifikasi gambar burung"
    ]
    for helpcom in list_command:
        await ctx.send(helpcom)

@bot.command()
async def birdspot(ctx):
    if ctx.message.attachments:
        for file in ctx.message.attachments:
            file_name = file.filename
            file_url = file.url
            await file.save(f"./{file_name}")
            await ctx.send(f"file berhasil disimpan dengan nama {file_name}")
            await ctx.send(f"anda dapat diakses di {file_url}")
            kelas, skor = get_class('keras_model.h5', 'labels.txt', f"./{file.filename}")

            #Inferensi

            if kelas == "pipit" and skor >= 0.75:
                await ctx.send("Ini adalah foto burung pipit, biasa tinggal di wilayah tropis Dunia Lama dan Australasia")

                await ctx.send("Burung pipit adalah sebuah omnivora, yang berarti mereka memakan berbagai jenis makanan. Makanan utama mereka adalah biji-bijian, tetapi mereka juga memakan serangga, buah-buahan, dan juga vertebrata kecil.")

            elif kelas == "merpati" and skor >= 0.75:
                await ctx.send("Ini adalah foto burung merpati, mereka dapat ditemukan di berbagai lingkungan. Diantaranya di perkotaan, hutan, padang rumput, gurun, dan daerah pesisir. Habitat asli mereka dulunya lebih banyak di daerah pantai, tetapi sekarang mereka telah beradaptasi dengan berbagai lingkungan, termasuk yang dekat dengan manusia")

                await ctx.send("Makanan burung merpati terdiri dari biji-bijian, buah-buahan, dan sayuran")
            
            elif kelas == "unta" and skor >= 0.75:
                await ctx.send("Ini adalah foto burung unta, mereka adalah burung terbesar dan terberat, dengan burung unta biasa dewasa memiliki berat antara 63.5 dan 145 kilogram, mereka banyak berhabitat di Afrika Selatan")

                await ctx.send("Makanan burung unta diantaranya ada tumbuhan seperti rumput, daun, buah-buahan, biji-bijian, dan akar. Mereka juga kadang memakan serangga, hewan pengerat kecil, ular, dan kadal. Uniknya, mereka menelan kerikil dan batu kecil untuk membantu menghancurkan makanan di dalam perut mereka, karena mereka tidak memiliki gigi.")
            
    else:
        await ctx.send('Anda belum mengirimkan file.')

bot.run("TOKEN")