# coding: -*- utf-8 -*-
import numpy as np
from sklearn.model_selection import train_test_split
# Chainer ���C�u�������g�p����
import chainer
# �����֐��Ƃ���Softmax�N���X�G���g���s�[�֐����g��
from chainer.functions.loss import softmax_cross_entropy
# �]���֐���accuracy���g��
from chainer.functions.evaluation import accuracy
# ml\data_processor.py����DataProcessor���C���|�[�g
from ml.data_processor import DataProcessor

# �g���[�i�[�N���X
class Trainer():

    # �R���X�g���N�^�����̊֐�
    # ���� model: ���f���N���X�C���X�^���X(�����ł�NumberRecognizeNN)
    # ���� resource: ���\�[�X�N���X�C���X�^���X(�����ł�Resource)
    # �߂�l�Ȃ�
    #
    # �����Q���C���X�^���X�ϐ��Q�֊i�[����
    def __init__(self, model, resource):
        self.model = model
        self.resource = resource

    # ���f���ɑ΂��ăg���[�j���O�����{���A���f����Ԃ��t�@�C���֕ۑ�����
    # ���� data: ���̓f�[�^
    # ���� target: �o�̓f�[�^�i�����f�[�^�j
    # ���� batch_size: �Pepoch�̃f�[�^�����A�f�t�H���g100
    # ���� epoch: epoch���A�f�t�H���g5��
    # ���� test_size: �f�t�H���g0.3(3�����e�X�g�f�[�^��)
    # ���� report_interval_epoch: ���|�[�g�쐬�Ԋu�A�f�t�H���g1�G�|�b�N
    def train(self, data, target, batch_size=100, epoch=5, test_size=0.3, report_interval_epoch=1):
        # �f�[�^�������[�e�B���e�B�N���X�𐶐�
        dp = DataProcessor()
        # �f�[�^�������[�e�B���e�B�N���X�̃C���X�^���X�ϐ���
        # ���K���p�����[�^�ŏ�����
        dp.set_normalization_params(data)
        # �f�[�^�������[�e�B���e�B�N���X�̐��K���p�����[�^���t�@�C���֕ۑ�
        self.resource.save_normalization_params(dp.means, dp.stds)
        # ���̓f�[�^data�ɑ΂��ăv�[�����O�����������A
        # ���ϒl�������ĕW���΍��l�Ŋ������l��ԋp����
        _data = dp.format_x(data)
        # �P���f�[�^�̏o�̓f�[�^target��v�f��int32�ŗv�f��1��
        # np.ndarray�^�z��ɕϊ�����
        _target = dp.format_y(target)
        # sklearn.model_selection��train_test_split�֐����g���āA
        # _data��_target����A
        # �P���f�[�^(train_x, train_y)�A�e�X�g�f�[�^(test_x, test_y)
        # �e�X�g�f�[�^��S�f�[�^�̂���test_size�����U�蕪��
        train_x, test_x, train_y, test_y = train_test_split(_data, _target, test_size=test_size)

        # Chainer���C�u�����̃I�v�e�B�}�C�U�N���XAdam()�𐶐�
        optimizer = chainer.optimizers.Adam()
        # ������z�z����N���A����ݒ�ɕύX
        optimizer.use_cleargrads()
        # �Ώۃ��f��(Chainer�����N)��ݒ肵�āA�I�v�e�B�}�C�U������������
        optimizer.setup(self.model)
        # loss�֐���lamda���Œ�`
        # ���� pred: �\���f�[�^
        # ���� teacher: ���t�f�[�^�i�����f�[�^�j
        # �߂�l: softmax_cross_entropy�ɂ������G���g���s�[����
        loss = lambda pred, teacher: softmax_cross_entropy.softmax_cross_entropy(pred, teacher)
        # batch_iter�̓o�b�`�f�[�^���P�����������o���ĕԂ�
        # �o�b�`�̏I���̏ꍇepoch_end��True���Ԃ��Ă���
        for x_batch, y_batch, epoch_end in dp.batch_iter(train_x, train_y, batch_size, epoch):
            # ���f���N���X��__call__�����s����
            # ��1�����̃o�b�`�f�[�^�ɑ΂����f�������s�����ʁi�\���f�[�^�j���擾
            predicted = self.model(x_batch)
            # �����֐��A�\���f�[�^�A�����f�[�^�������ɗ^���œK�������s
            optimizer.update(loss, predicted, y_batch)
            # epoc�I���̏ꍇ
            if epoch_end:
                # ���o�b�`�f�[�^��acuuracy���擾
                train_acc = accuracy.accuracy(predicted, y_batch)
                # �œK����̏�ԂŃe�X�g�f�[�^�ŗ\��
                predicted_to_test = self.model(test_x)
                # �e�X�g�f�[�^��acuuracy���擾
                test_acc = accuracy.accuracy(predicted_to_test, test_y)
                # accuracy��stdout�֏o��
                print("train accuracy={}, test accuracy={}".format(train_acc.data, test_acc.data))
                # Resource�N���X�̃��f���ۑ��֐��Ō����_�̃��f����ԕۑ�
                self.resource.save_model(self.model)
