from PIL import Image

def encode_image(image_path, secret_message, output_path):
    # Importa o módulo Image da biblioteca PIL para trabalhar com imagens

    # Abre a imagem para codificação
    img = Image.open(image_path)
    # Carrega a imagem a partir do caminho fornecido
    width, height = img.size
    # Obtém as dimensões da imagem (largura e altura)

    # Verifica se a imagem tem espaço suficiente para a mensagem
    total_pixels = width * height
    max_bytes = total_pixels // 8
    # Calcula o número máximo de bytes que a imagem pode acomodar (considerando 8 bits por byte)
    msg_bytes = bytes(secret_message, 'utf-8')
    # Converte a mensagem secreta em uma sequência de bytes usando codificação UTF-8
    msg_size = len(msg_bytes)
    # Obtém o tamanho da mensagem em bytes
    if msg_size > max_bytes:
        raise ValueError("A mensagem é muito grande para ser codificada na imagem.")
    # Verifica se a mensagem é maior do que o espaço disponível na imagem e levanta um erro caso seja

    # Converte a mensagem em uma sequência de bits
    bit_msg = ''.join(format(byte, '08b') for byte in msg_bytes)
    # Converte cada byte da mensagem em uma sequência de 8 bits (representação binária)

    # Codifica os bits da mensagem nos bits menos significativos dos pixels da imagem
    encoded_img = img.copy()
    pixel_index = 0
    for y in range(height):
        for x in range(width):
            if pixel_index < len(bit_msg):
                pixel = list(img.getpixel((x, y)))
                for i in range(3):
                    if pixel_index < len(bit_msg):  # Verifica se pixel_index ainda é menor que o comprimento de bit_msg
                        if pixel[i] % 2 == 0 and bit_msg[pixel_index] == '1':
                            pixel[i] += 1
                        elif pixel[i] % 2 == 1 and bit_msg[pixel_index] == '0':
                            pixel[i] -= 1
                        pixel_index += 1
                    else:
                        break  # Sai do loop interno se pixel_index exceder o comprimento de bit_msg
                encoded_img.putpixel((x, y), tuple(pixel))
            else:
                break  # Sai do loop externo se pixel_index exceder o comprimento de bit_msg
    # Salva a imagem codificada
    encoded_img.save(output_path)
    # Salva a imagem codificada no caminho de saída fornecido
    print(f"Steganography applyed succesfully. Image saved in {output_path}")


def decode_image(image_path):
    # Abre a imagem para decodificação
    img = Image.open(image_path)
    width, height = img.size

    # Decodifica os bits menos significativos dos pixels da imagem para recuperar a mensagem
    bit_msg = ''
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                bit_msg += str(pixel[i] % 2)

    # Encontra o limite que indica o fim da mensagem
    limit_index = bit_msg.find('00000000')  # Encontra o primeiro '00000000' na sequência de bits
    bit_msg = bit_msg[:limit_index]  # Obtém os bits até o limite

    # Converte a sequência de bits de volta para a mensagem original como bytes
    msg_bytes = bytearray()
    for i in range(0, len(bit_msg), 8):
        byte = int(bit_msg[i:i+8], 2)
        msg_bytes.append(byte)

    secret_message = msg_bytes

    print(f"Secret message extracted. Your message is: {secret_message}")
