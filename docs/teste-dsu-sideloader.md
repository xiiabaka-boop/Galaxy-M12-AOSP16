# Plano de teste GSI via DSU Sideloader — Galaxy M12 (SM-M127F)

Este projeto é de **testes por DSU** (Dynamic System Updates), não de flash permanente em `super` ou `system`.

## O que muda

- DSU instala temporariamente uma imagem de sistema e um ambiente de dados separados, sem substituir a partição original de sistema.
- Em um teste normal, reiniciar permite voltar ao Android original; isso **não é garantia absoluta de recuperação se houver falha no boot**.
- A GSI continua usando kernel/boot, `vendor`, `odm`, rádio e serviços de hardware do aparelho. Portanto, o DSU **não resolve por si só** problemas VINTF/kernel e HAL.
- Para a imagem atual, a análise estática encontrou uma incompatibilidade potencial relevante entre o kernel ativo 4.19 e as entradas 5.4 da matriz FCM 5. Veja [relatório técnico](gsi-vendor-compatibility.md). Não interpretar isso como teste real de boot.

## DSU Sideloader

Projeto: https://github.com/VegaBobo/DSU-Sideloader

Conforme o README do aplicativo, são aceitos `xz`, `gz`, `img` e `zip` (ZIP somente em formato de pacote DSU). **A Release atual já fornece `.img.xz`**, então não há necessidade de convertê-la em ZIP genérico ou gravar a partição `super`.

O aparelho apresenta Treble e partições dinâmicas, bootloader desbloqueado e Magisk (informados pelo proprietário). Isso atende várias condições de entrada, mas a capacidade real de iniciar uma GSI depende dos detalhes do firmware.

## Etapas de teste seguro

1. Salvar dados pessoais e verificar espaço livre suficiente no armazenamento.
2. Confirmar que o DSU Sideloader realmente consegue instalar **e iniciar** uma GSI conhecida como compatível no aparelho; se existir histórico, registrar modelo da imagem e resultado.
3. Manter o modo de inicialização temporária; **não ativar sticky mode** antes de um primeiro boot bem-sucedido.
4. Não alterar `vbmeta`, `vendor`, `odm`, boot ou SELinux automaticamente.
5. Se houver erro, anotar a fase exata: preparação, instalação, reboot/boot, interface, rede, câmera ou retorno ao sistema.
6. Compartilhar logs minimizados do DSU apenas após inspecionar dados pessoais e informações de conta.
7. Se não houver método de recuperação confiável, evitar testes com imagens conhecidamente incompatíveis.

## Estado deste projeto

- GSI `aosp-arm64-ab-vanilla-16.0-20250625.img.xz` hospedada no GitHub Releases.
- Integridade SHA-256 confirmada contra a cópia local do usuário.
- Análise somente leitura dos XMLs `vendor` e da GSI concluída.
- **Ainda não existe imagem modificada e validada para o SM-M127F.**
- O formato `.img.xz` é adequado como entrada do DSU Sideloader; isso não implica compatibilidade de inicialização.

Referências: [DSU oficial](https://developer.android.com/topic/dsu), [DSU Sideloader](https://github.com/VegaBobo/DSU-Sideloader), [regras Android VINTF](https://source.android.com/docs/core/architecture/vintf/match-rules).
