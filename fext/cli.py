import os

import click
import cv2 as cv

from fext.video import Video

def generate_filename(output_folder, prefix, number):
    filename = "{0}{1}.jpg".format(prefix, number)
    return os.path.join(output_folder, filename)

@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.option('--output', '-o', default='', type=click.Path(exists=True))
@click.option('--interval', '-i', default=10)
@click.option('--prefix', '-p', default=None)
def main(src, output, interval, prefix):
    video = Video(src)
    number_images = len(video) // (interval * video.fps)
    prefix = prefix or os.path.basename(src)

    click.echo('Video length: {}'.format(video.time))
    click.echo('Number of images: {}'.format(number_images))

    with click.progressbar(length=len(video), label='Generating images') as bar:
        for pos, image in video.frames(interval):
            filepath = generate_filename(output, prefix, video.curr_frame)
            cv.imwrite(filepath, image)
            bar.update(video.curr_frame)

    video.release()
