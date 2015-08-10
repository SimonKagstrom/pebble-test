import os.path

top = '.'
out = 'build'

def options(ctx):
    ctx.load('pebble_sdk')

def configure(ctx):
    ctx.load('pebble_sdk')

    CROSS_COMPILE_PREFIX = 'arm-none-eabi-'
    ctx.env.CXX = CROSS_COMPILE_PREFIX+'g++'
    ctx.load('g++')

    ctx.env.CXXFLAGS = list(ctx.env.CFLAGS)
    ctx.env.CXXFLAGS.remove('-std=c99')
    
    sdk_folder = ctx.root.find_dir(ctx.env['PEBBLE_SDK'])
    ctx.env.CXXFLAGS.extend(['-std=c++11', '-fPIE', '-fno-unwind-tables', '-fno-exceptions', '-fno-rtti'])

def build(ctx):
    ctx.load('pebble_sdk')

    build_worker = os.path.exists('worker_src')
    binaries = []

    for p in ctx.env.TARGET_PLATFORMS:
        ctx.set_env(ctx.all_envs[p])
        app_elf='{}/pebble-app.elf'.format(ctx.env.BUILD_DIR)
        ctx.pbl_program(source=['src/main.c', 'src/kalle.c', 'src/manne.cpp'], target=app_elf)

        if build_worker:
            worker_elf='{}/pebble-worker.elf'.format(ctx.env.BUILD_DIR)
            binaries.append({'platform': p, 'app_elf': app_elf, 'worker_elf': worker_elf})
            ctx.pbl_worker(source=ctx.path.ant_glob('worker_src/**/*.cc'),
            target=worker_elf)
        else:
            binaries.append({'platform': p, 'app_elf': app_elf})

    ctx.pbl_bundle(binaries=binaries, js=ctx.path.ant_glob('src/js/**/*.js'))
