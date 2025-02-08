# python で動かす連射ツール
試作品
開発環境きれいに整備するとかの練習兼用


## pyenv と venv で python のバージョンとモジュールの仮想環境を作る
- [pyenv: python のバージョン管理](https://github.com/pyenv-win/pyenv-win)
- venv: モジュール含めての仮想環境

```
# pyenv の確認(3.13.1 を使う)
pyenv version

# venv の確認

# 仮想環境作るだけなので１回でいい
python -m venv .venv-python-rapid-fire

# アクティベート
.\.venv-python-rapid-fire\Scripts\activate
```