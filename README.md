# Player Proxy

A proxy for media player, configure file open rule, and open file with different media player.

For example:

1. rule A -> folder `/path/to/testA` -> opened by player `MPV`;
2. rule B -> folder `/path/to/testB` -> opened by player `MPC-BE`;
3. rule C -> folder `/path/to/testC` -> opened by player `PotPlayer`.

When double click file under `/path/to/testA/*`, player-proxy will automatically match the rule and open it with `MPV`.

## Usage

1. Download the latest application
   on [https://github.com/akiakise/player-proxy/releases](https://github.com/akiakise/player-proxy/releases)

2. Open `player-proxy.exe` and add your own rules:
   ![config](resources/1-config.png)

3. Always open video files with `player-proxy.exe`:
   ![association](resources/2-association.png)

4. Open your video file and have a nice day.

## LICENSE

[MIT](LICENSE)
