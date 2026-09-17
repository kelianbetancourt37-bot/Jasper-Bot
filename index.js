const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const { exec } = require('child_process');

async function iniciarBot() {
    const { state, saveCreds } = await useMultiFileAuthState('Qrcode_Sesion');

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);

    if (!sock.authState.creds.registered) {
        const numeroLimpio = "5595984017858";
        
        console.log('Generando código de vinculación para +55 95 98401-7858...');
        setTimeout(async () => {
            try {
                const code = await sock.requestPairingCode(numeroLimpio);
                console.log(`\n TU CÓDIGO DE VINCULACIÓN ES: ${code}\n`);
            } catch (err) {
                console.error('Error al generar el código:', err.message);
            }
        }, 3000);
    }

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update;

        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) iniciarBot();
        } else if (connection === 'open') {
            console.log(' ¡Bot conectado con éxito!');
        }
    });

    sock.ev.on('messages.upsert', async (m) => {
        const msg = m.messages[0];
        if (!msg.message) return;

        const texto = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
        const remitente = msg.key.remoteJid;

        if (texto.startsWith('.')) {
            const partes = texto.trim().split(' ');
            const comandoBruto = partes[0].toLowerCase();
            const comando = comandoBruto.startsWith('.') ? comandoBruto.slice(1) : comandoBruto;
            const parametro = partes.slice(1).join(' ') || '';
            
            const usuarioId = msg.key.participant || remitente;

            // COMANDOS DE ADMINISTRACIÓN DE GRUPOS EN WHATSAPP
            if (remitente.endsWith('@g.us')) {
                try {
                    const groupMetadata = await sock.groupMetadata(remitente);
                    const participantes = groupMetadata.participants || [];
                    
                    const esAdmin = participantes.some(p => 
                        (p.id === usuarioId || p.id === msg.key.participant) && 
                        (p.admin === 'admin' || p.admin === 'superadmin')
                    );

                    if (comando === 'close' || comando === 'open') {
                        if (!esAdmin) {
                            await sock.sendMessage(remitente, { text: '⚠️ Solo los administradores del grupo pueden usar este comando.' }, { quoted: msg });
                            return;
                        }

                        if (comando === 'close') {
                            await sock.groupSettingUpdate(remitente, 'announcement');
                            await sock.sendMessage(remitente, { text: '🔒 El grupo ha sido cerrado. Solo administradores pueden enviar mensajes.' }, { quoted: msg });
                            return;
                        } 
                        if (comando === 'open') {
                            await sock.groupSettingUpdate(remitente, 'not_announcement');
                            await sock.sendMessage(remitente, { text: '🔓 El grupo ha sido abierto. Todos pueden enviar mensajes.' }, { quoted: msg });
                            return;
                        }
                    }
                } catch (err) {
                    console.error('Error al gestionar metadatos del grupo:', err.message);
                    await sock.sendMessage(remitente, { text: '⚠️ Error: Asegúrate de que el bot sea Administrador del grupo.' }, { quoted: msg });
                    return;
                }
            }

            // COMANDOS PROCESADOS DESDE PYTHON (Usando 'python' para Windows)
            const comandoPython = `python bot.py ".${comando}" "${parametro}" "${usuarioId}"`;
            
            exec(comandoPython, { encoding: 'utf-8' }, async (error, stdout) => {
                if (error) {
                    console.error(`Error ejecutando Python: ${error.message}`);
                    return;
                }
                
                const respuesta = stdout.trim();
                
                if (respuesta) {
                    try {
                        if (respuesta.startsWith("GIF|")) {
                            const partesGif = respuesta.split("|");
                            const urlGif = partesGif[1];
                            const mensajeTexto = partesGif[2] || "";

                            await sock.sendMessage(remitente, {
                                video: { url: urlGif },
                                caption: mensajeTexto,
                                gifPlayback: true
                            }, { quoted: msg });

                        } else if (respuesta.includes("[IMAGEN:")) {
                            const partesImg = respuesta.split("\n[IMAGEN:");
                            const mensajeTexto = partesImg[0];
                            const urlImagen = partesImg[1].replace("]", "").trim();

                            await sock.sendMessage(remitente, {
                                image: { url: urlImagen },
                                caption: mensajeTexto
                            }, { quoted: msg });

                        } else {
                            await sock.sendMessage(remitente, { text: respuesta }, { quoted: msg });
                        }
                    } catch (sendErr) {
                        console.error('Error al enviar el mensaje por WhatsApp:', sendErr.message);
                    }
                }
            });
        }
    });
}

iniciarBot();