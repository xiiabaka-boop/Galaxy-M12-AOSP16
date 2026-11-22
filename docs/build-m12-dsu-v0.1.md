# M12 AOSP16 DSU v0.1 — primeira GSI modificada (experimental)

**Esta variante altera a GSI AOSP 16 original, mas NÃO é uma ROM adaptada e validada por testes.**

## Origem

- Base: `aosp-arm64-ab-vanilla-16.0-20250625.img.xz`
- SHA-256 verificado na Release base: `f3abc15e85fb3d8050881c0710259f8e12baf8fd5cf05598e672073b7816c831`
- [Release original](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/releases/tag/aosp16-base)
- [Workflow de build](../.github/workflows/build-m12-dsu.yml)
- [Script do ajuste](../scripts/patch_m12_display.py)

## Alteração de v0.1

Apenas `ro.sf.lcd_density=300` em `/system/build.prop`, com o valor de 300 usado no [BoardConfig.mk do M12 LineageOS 21](https://github.com/galaxym12development/android_device_samsung_m12/blob/lineage-21/BoardConfig.mk). Pode modificar a escala da interface, **mas essa propriedade pode ser substituída pelo firmware vendor**.

A imagem original inclui EXT4 `shared_blocks` (somente leitura). O workflow usa `e2fsck -E unshare_blocks` antes de editar, redimensiona um pouco a imagem para abrir espaço, modifica o arquivo existente sem substituí-lo (preservando permissões e rótulos SELinux do inode), roda `e2fsck`, monta de novo somente leitura para conferir, compacta com XZ e testa o arquivo comprimido. Se alguma verificação falhar, o workflow para sem publicar uma imagem quebrada.

## O que não muda

- Kernel/bootloader, DTB, DTBO, partições `vendor` e `odm`, modem, câmera, áudio, Wi-Fi.
- SELinux, AVB/vbmeta, permissões privilegiadas, permissividade do adb.
- Não é garantido o boot. A evidência de uma **outra GSI Android 16 que já iniciou via DSU** no SM-M127F é relevante, mas ainda não identificamos qual foi a imagem funcional.

## Como obter

**O workflow terminou com sucesso e publicou** a [prerelease de testes `m12-dsu-v0.1`](https://github.com/xiiabaka-boop/Galaxy-M12-AOSP16/releases/tag/m12-dsu-v0.1), contendo `aosp16-m12-dsu-v0.1.img.xz` e o arquivo `.sha256`. Se der erro, não existirá uma versão publicada; abra os logs do workflow.

## Teste por DSU Sideloader

- Selecione o `.img.xz` baixado no DSU Sideloader, **não** faça flash por Odin nem grave no `super`.
- Salve dados importantes e confirme que consegue retornar ao sistema original.
- Não use **Sticky Mode** na primeira execução.
- Anote se a GSI instala, inicia e se tela, toque, Wi-Fi, rede móvel, áudio e câmera funcionam.
- Não modifique `vbmeta`, `vendor`, kernel ou SELinux apenas para forçar a inicialização.

**É um build experimental de validação da cadeia de modificação e DSU, não uma ROM pronta.** Os próximos patches dependem dos resultados do dispositivo.
