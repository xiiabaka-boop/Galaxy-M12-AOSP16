# AOSP Android 16 no Galaxy M12 (SM-M127F)

**Situação atual: análise técnica. Ainda NÃO é uma ROM comprovadamente inicializável.**

**Atualização:** o proprietário informou que **já iniciou uma GSI Android 16 pelo DSU Sideloader** neste Galaxy M12. Ainda não sabemos qual imagem foi usada ou se é a mesma desta Release. O diagnóstico estático identificou uma possível diferença entre kernel 4.19 e a matriz FCM 5 com entradas 5.4, mas isso **não prova que Android 16 não possa iniciar no aparelho**. Confira o [relatório técnico atualizado](docs/gsi-vendor-compatibility.md).

Este projeto tenta avaliar uma GSI AOSP 16 para um Samsung Galaxy M12 (SM-M127F) com Android 13 original e Magisk. O bootloader está desbloqueado, segundo o proprietário.

## O que foi concluído

- A GSI compactada foi enviada ao [GitHub Releases](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/releases/tag/aosp16-base).
- O SHA-256 da cópia do celular corresponde ao da Release: `f3abc15e85fb3d8050881c0710259f8e12baf8fd5cf05598e672073b7816c831`.
- O GitHub Actions verificou o XZ, extraiu e montou a imagem EXT de aproximadamente 2,3 GiB **somente para leitura**.
- Foram identificados arquivos VINTF, APEX, SELinux e configuração de inicialização da GSI.
- As árvores do LineageOS 19.1, 21 e um branch comunitário `a16-lts` foram estudadas como referências, **não** copiadas para a imagem.

Não verificamos a origem oficial do arquivo (assinatura/checksum do autor original), nem iniciamos **esta imagem específica** no aparelho. O dono do M12 relatou inicialização bem-sucedida de **outra ou possivelmente esta** GSI Android 16 pelo DSU (identidade pendente).

## Nosso método de teste: DSU Sideloader

O proprietário informou que irá testar a GSI pelo **DSU Sideloader**, sem flash permanente do `system.img`. O programa aceita a imagem `.img.xz` publicada, mas o DSU continua usando o kernel e drivers do dispositivo. Temos uma possível incompatibilidade VINTF, então o formato aceito não equivale a compatibilidade de boot. Veja o [plano de testes DSU](docs/teste-dsu-sideloader.md).

## O que ainda falta

- Identificar o nome, a origem e o resultado de funcionamento da GSI Android 16 que já iniciou pelo DSU.
- Comparar as interfaces e possíveis patches dessa GSI funcional com a imagem da Release (documentação VINTF `vendor` e `odm` já foi coletada e analisada).
- Validar ambiente de recuperação (backup e acesso confiável ao modo Download) antes de qualquer teste de inicialização.
- Somente então criar e testar *patches* individualizados, reversíveis, com descrição e evidência.

## Coleta segura de dados do M12 pelo Termux

O script de coleta está em [scripts/m12-vendor-snapshot.sh](scripts/m12-vendor-snapshot.sh). Leia-o antes de executá-lo. Ele **não** grava nem altera as partições do Android; lê propriedades e copia apenas arquivos XML de configuração VINTF para uma pasta de diagnóstico.

No Termux:

```sh
curl -fL https://raw.githubusercontent.com/xiiabaka-boop/Galaxy-M12-AOSP16/main/scripts/m12-vendor-snapshot.sh -o m12-vendor-snapshot.sh
su -c "sh $HOME/m12-vendor-snapshot.sh /sdcard/Download/m12-vendor-snapshot"
```

Depois, se não houver erros:

```sh
su -c 'cd /sdcard/Download && tar -czf m12-vendor-snapshot.tar.gz m12-vendor-snapshot'
```

O arquivo `m12-vendor-snapshot.tar.gz` poderá ser compartilhado para análise. **Confira o conteúdo antes**: não envie IMEI, número de série, dados de conta, partições EFS ou `persist`. O script não tenta coletar esses dados.

## Não instale ainda

Uma GSI com SHA-256 válido não garante compatibilidade de HAL, kernel, partições ou SELinux. Não desabilite AVB/SELinux, não substitua `vendor` e não grave em `super` apenas com base nesses relatórios.
