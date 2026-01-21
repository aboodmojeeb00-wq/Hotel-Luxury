import os

base_dir = r'd:/Django/myvenv/A/A'
settings_path = os.path.join(base_dir, 'settings.py')
urls_path = os.path.join(base_dir, 'urls.py')

try:
    with open(settings_path, 'r') as f:
        content = f.read()
    if "'User'" not in content:
        content = content.replace("'hotel',", "'hotel',\n    'User',")
        with open(settings_path, 'w') as f:
            f.write(content)
        print('Updated settings.py')
    else:
        print('settings.py already has User')
except Exception as e:
    print(f'Error updating settings: {e}')

try:
    with open(urls_path, 'r') as f:
        content = f.read()
    if 'User.urls' not in content:
        target = "path('', include('hotel.urls')),"
        replacement = "path('', include('hotel.urls')),\n    path('user/', include('User.urls')),"
        if target in content:
            content = content.replace(target, replacement)
            with open(urls_path, 'w') as f:
                f.write(content)
            print('Updated urls.py')
        else:
            print('Could not find insertion point in urls.py')
    else:
        print('urls.py already has User.urls')
except Exception as e:
    print(f'Error updating urls: {e}')
