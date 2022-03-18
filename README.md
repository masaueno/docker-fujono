まず手元pcで

```bash
xhost +
```

これ危険だからよくない
終わったら

```bash
xhost -
```

しとく
それから

```bash
hostname
```

を実行し、出てきた名前覚えといて

つぎに

```bash
docker-compose build
docker-compose up
```

で、コンテナ立ち上げ

そしたら別たぶで、

```bash
docker-compose exec python3 bash
```

で、コンテナに入ったら、

```bash
export DISPLAY=(ここに最初に覚えたやついれる):0
cd handpose3d
python handpose3d.py
```
