<div align="center">

# Music Game

<br>
<div>
    <img alt="python-pygame" src="https://img.shields.io/pypi/pyversions/pygame">
</div>
<div>
    <img alt="platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blueviolet">
</div>
<div>
    <img alt="commit" src="https://img.shields.io/github/commit-activity/m/11375071/music_game">
    <img alt="stars" src="https://img.shields.io/github/stars/11375071/music_game?style=social">
</div>
<br>

</div>

## Run with Python

```shell
python src/main.py  # to run
```

## TODO

### Feature

- [x] 完善选曲界面 menu
- [ ] 制作评价结算界面
- [ ] 完善 PTT 以及最优分数保存

### Optimize

- [ ] 添加歌曲前的几秒等待

### Code

- [x] 学习 pygame.sprite，看看能否用来简化代码结构，比如不用写一大堆 xxxButton.render() 和 event_check() 语句  
      > 未使用 pygame.sprite，直接使用 page 类就可以实现
- [x] 将 play, play_pause, offset_guide 三个页面用 page 类简化
- [x] 完全简化所有 obj 对象的共同函数
- [ ] Song 改为文件夹自动搜索，而非手打

### 美工

- [ ] 美化界面，降低读谱压力
- [ ] 选曲界面改为图片样式（现在是随机色块）
