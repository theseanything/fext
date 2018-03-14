import os

import click
import cv2 as cv

from fext.video import Video

def generate_filename(output_folder, prefix, number):
    filename = "{0}{1}.jpg".format(prefix, number)
    return os.path.join(output_folder, filename)

@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.option('--folder', '-f', default='', type=click.Path(exists=True))
@click.option('--interval', '-i', default=10.0)
@click.option('--prefix', '-p', default=None)
@click.option('--dry-run', '-d', is_flag=True)
def main(src, folder, interval, prefix, dry_run):
    video = Video(src)
    number_images = int(len(video) // (interval * video.fps))
    prefix = prefix or os.path.basename(src)

    click.echo('Video length: {}'.format(video.time))
    click.echo('Number of images: {}'.format(number_images))
    click.echo('Dimensions: {} H x {} W'.format(video.height, video.width))

    label = 'Generating images'

    if not dry_run:
        with click.progressbar(length=len(video), label=label) as bar:
            for pos, image in video.frames(interval):
                filepath = generate_filename(folder, prefix, pos)
                cv.imwrite(filepath, image)
                bar.update(pos)

    click.echo('Releasing video...')
    video.release()
