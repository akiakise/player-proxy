# FAE

File Association Enhancement.

I have two video player, `MPC-BE` for anime, `PotPlayer` for most of the others. However, I can only specify one default
app for video files, such as `.mkv`, `.mp4`
and so on.

So I consider enhancing the file association, using a simple python script to associate with video files, and detect
which app should be used to open the file.

That is FAE. Now it is just checking whether the path of file contains `param`. It is enough to me, now.

## Usage

### 1. Create your own configuration file.

Make a copy of [fae.sample.json](fae.sample.json), named `fae.json`, change the config items:

```json
{
  "param": "path content for matching",
  "app": "/path/to/app/when/matched",
  "fallback": "/path/to/app/when/not/matched"
}
```

How does the config items work? See the pseudo-code:

```py
if param in file_path:
    subprocess.run(app, file_path)
else:
    subprocess.run(fallback, file_path)
```

### 2. Build a executable file

```shell
pip3 install pyinstaller
pyinstaller.exe --onedir --noconsole --noconfirm --add-data "fae.json;." judge.py
```

### 3. Change your default app

![default app](resources/default_app.png)

## LICENSE

[MIT](LICENSE)
