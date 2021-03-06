import os
import pprint
import tensorflow as tf

from data import read_data
from model.nnlm import NNLM

pp = pprint.PrettyPrinter()

flags = tf.app.flags

flags.DEFINE_integer("word_dim", 60, "word embeding dimension [60]")
flags.DEFINE_integer("hidden_num", 50, "number of hidden states [50]")
flags.DEFINE_integer("batch_size", 10, "batch size to use during training [120]")
flags.DEFINE_integer("num_epochs", 5, "number of epoch to use during training [5]")
flags.DEFINE_string("win_size", 5, "the order of model [5]")
flags.DEFINE_float("grad_clip", 50, "clip gradients to this norm [50]")
flags.DEFINE_string("data_dir", "data", "data directory [data]")
flags.DEFINE_string("data_name", "ptb", "data set name [ptb]")
flags.DEFINE_boolean("is_test", False, "True for testing, False for Training [False]")
flags.DEFINE_boolean("show", False, "print progress [False]")
flags.DEFINE_string("logdir", ".", "log directory")

FLAGS = flags.FLAGS

def main(_):
    count = []
    word2idx = {}

#    if not os.path.exists(FLAGS.checkpoint_dir):
#      os.makedirs(FLAGS.checkpoint_dir)

    train_data = read_data('%s/%s.train.txt' % (FLAGS.data_dir, FLAGS.data_name), count, word2idx)
    valid_data = read_data('%s/%s.valid.txt' % (FLAGS.data_dir, FLAGS.data_name), count, word2idx)
    test_data = read_data('%s/%s.test.txt' % (FLAGS.data_dir, FLAGS.data_name), count, word2idx)

    idx2word = dict(zip(word2idx.values(), word2idx.keys()))
    FLAGS.nwords = len(word2idx)

    pp.pprint(flags.FLAGS.__flags)

    with tf.Session() as sess:
        model = NNLM(FLAGS, sess)
        model.build_model()

        if FLAGS.is_test:
            model.run(valid_data, test_data)
        else:
            model.run(train_data, valid_data)

if __name__ == '__main__':
    tf.app.run()
