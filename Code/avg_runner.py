import tensorflow as tf
import getopt
import sys
import csv
import os

from utils import get_batch
from d_model import DiscriminatorModel
from g_model import GeneratorModel
import constants as c


class AVGRunner:
    def __init__(self, model_load_path, num_test_rec):
        """
        Initializes the Adversarial Video Generation Runner.

        @param model_load_path: The path from which to load a previously-saved model.
                                Default = None.
        @param num_test_rec: The number of recursive generations to produce when testing. Recursive
                             generations use previous generations as input to predict further into
                             the future.
        """

        self.global_step = 0
        self.num_test_rec = num_test_rec

        self.sess = tf.Session()
        self.summary_writer = tf.train.SummaryWriter(c.SUMMARY_SAVE_DIR, graph=self.sess.graph)

        if c.ADVERSARIAL:
            print 'Init discriminator...'
            self.d_model = DiscriminatorModel(self.sess,
                                              self.summary_writer,
                                              c.FRAME_HEIGHT,
                                              c.FRAME_WIDTH,
                                              c.SCALE_CONV_FMS_D,
                                              c.SCALE_KERNEL_SIZES_D,
                                              c.SCALE_FC_LAYER_SIZES_D)

        print 'Init generator...'
        self.g_model = GeneratorModel(self.sess,
                                      self.summary_writer,
                                      c.FRAME_HEIGHT,
                                      c.FRAME_WIDTH,
                                      c.SCALE_FC_LAYER_SIZES_G,
                                      c.SCALE_CONV_FMS_G,
                                      c.SCALE_KERNEL_SIZES_G)

        print 'Init variables...'
        self.saver = tf.train.Saver(keep_checkpoint_every_n_hours=2)
        self.sess.run(tf.initialize_all_variables())

        # if load path specified, load a saved model
        if model_load_path is not None:
            self.saver.restore(self.sess, model_load_path)
            print 'Model restored from ' + model_load_path

    def train(self, num_epochs = 1):
        """
        Runs a training loop on the model networks.
        """
        with open(c.TRAIN_PATH, 'rb') as train_file:
            reader = csv.reader(train_file)

            # num lines to skip in loop (because they will be read as part of the batch getter)
            skip_lines = c.BATCH_SIZE if c.ADVERSARIAL else 2 * c.BATCH_SIZE
            for epoch in xrange(num_epochs):
                for row_num in xrange(0, c.NUM_TRAIN, skip_lines):
                    if c.ADVERSARIAL:
                        # update discriminator
                        batch = get_batch(reader)
                        print 'Training discriminator...'
                        self.d_model.train_step(batch, self.g_model)

                    # update generator
                    batch = get_batch(reader)
                    print 'Training generator...'
                    self.global_step = self.g_model.train_step(
                        batch, discriminator=(self.d_model if c.ADVERSARIAL else None))

                    # save the models
                    if self.global_step % c.MODEL_SAVE_FREQ == 0:
                        print '-' * 30
                        print 'Saving models...'
                        self.saver.save(self.sess,
                                        os.path.join(c.MODEL_SAVE_DIR, 'model.ckpt'),
                                        global_step=self.global_step)
                        print 'Saved models!'
                        print '-' * 30

                    # # test generator model
                    # if self.global_step % c.TEST_FREQ == 0:
                    #     self.test()

    # def test(self):
    #     """
    #     Runs one test step on the generator network.
    #     """
    #     batch = get_test_batch(c.BATCH_SIZE, num_rec_out=self.num_test_rec)
    #     self.g_model.test_batch(
    #         batch, self.global_step, num_rec_out=self.num_test_rec)


def usage():
    print 'Options:'
    print '-l/--load_path=    <Relative/path/to/saved/model>'
    print '-r/--recursions=   <# recursive predictions to make on test>'
    print '-a/--adversarial=  <{t/f}> (Whether to use adversarial training. Default=True)'
    print '-n/--name=         <Subdirectory of ../Data/Save/*/ in which to save output of this run>'
    print '-O/--overwrite     (Overwrites all previous data for the model with this save name)'
    print '-T/--test_only     (Only runs a test step -- no training)'
    print '-H/--help          (Prints usage)'
    print '--stats_freq=      <How often to print loss/train error stats, in # steps>'
    print '--summary_freq=    <How often to save loss/error summaries, in # steps>'
    print '--img_save_freq=   <How often to save generated images, in # steps>'
    print '--test_freq=       <How often to test the model on test data, in # steps>'
    print '--model_save_freq= <How often to save the model, in # steps>'


def main():
    ##
    # Handle command line input.
    ##

    load_path = None
    test_only = False
    num_test_rec = 1  # number of recursive predictions to make on test
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'l:r:a:n:OTH',
                                ['load_path=', 'recursions=', 'adversarial=', 'name=', 'overwrite',
                                 'test_only', 'help', 'stats_freq=', 'summary_freq=',
                                 'img_save_freq=', 'test_freq=', 'model_save_freq='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l', '--load_path'):
            load_path = arg
        if opt in ('-r', '--recursions'):
            num_test_rec = int(arg)
        if opt in ('-a', '--adversarial'):
            c.ADVERSARIAL = (arg.lower() == 'true' or arg.lower() == 't')
        if opt in ('-n', '--name'):
            c.set_save_name(arg)
        if opt in ('-O', '--overwrite'):
            c.clear_save_name()
        if opt in ('-H', '--help'):
            usage()
            sys.exit(2)
        if opt in ('-T', '--test_only'):
            test_only = True
        if opt == '--stats_freq':
            c.STATS_FREQ = int(arg)
        if opt == '--summary_freq':
            c.SUMMARY_FREQ = int(arg)
        if opt == '--img_save_freq':
            c.IMG_SAVE_FREQ = int(arg)
        if opt == '--test_freq':
            c.TEST_FREQ = int(arg)
        if opt == '--model_save_freq':
            c.MODEL_SAVE_FREQ = int(arg)

    ##
    # Init and run the predictor
    ##

    runner = AVGRunner(load_path, num_test_rec)
    # if test_only:
    #     runner.test()
    # else:
    runner.train()


if __name__ == '__main__':
    main()
