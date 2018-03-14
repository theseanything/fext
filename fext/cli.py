import os
from statistics import mean, pvariance

import click
import cv2 as cv
import numpy

from fext.video import Video

def generate_filename(output_folder, prefix, number):
    filename = "{0}{1}.jpg".format(prefix, number)
    return os.path.join(output_folder, filename)

def calc_blur(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    laplacian = cv.Laplacian(image, cv.CV_64F)
    return numpy.var(laplacian)

@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.option('--folder', '-f', default='', type=click.Path(exists=True))
@click.option('--interval', '-i', default=10.0)
@click.option('--prefix', '-p', default=None)
@click.option('--dry-run', '-d', is_flag=True)
@click.option('--blur-threshold', '-b', default=0)
def main(src, folder, interval, prefix, dry_run, blur_threshold):
    video = Video(src)
    number_images = int(len(video) // (interval * video.fps))
    prefix = prefix or os.path.basename(src)

    click.echo('Video length: {}'.format(video.time))
    click.echo('Number of images: {}'.format(number_images))
    click.echo('Dimensions: {} H x {} W'.format(video.height, video.width))

    label = 'Generating images'

    blur_scores = []
    skipped_frames = {
        'blurry': 0
    }
    blurry = False

    with click.progressbar(length=len(video), label=label) as bar:
        frame_interval = interval * video.fps
        for pos, image in video.frames(frame_interval):
            bar.update(frame_interval)
            if blur_threshold:
                blur = calc_blur(image)
                blur_scores.append(float(blur))
                if blur < blur_threshold:
                    skipped_frames['blurry'] += 1
                    continue
            if not dry_run:
                filepath = generate_filename(folder, prefix, pos)
                cv.imwrite(filepath, image)


    video.release()

    if blur_threshold:
        click.echo('Skipped frames: {}'.format(skipped_frames))
        click.echo('Average blur score: {}'.format(mean(blur_scores)))
