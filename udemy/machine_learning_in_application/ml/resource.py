# coding: -*- utf-8 -*-
import os
import json
from datetime import datetime
import numpy as np
from chainer import serializers
from ml.data_processor import DataProcessor

# Resource �N���X
#
# ���f���p�����[�^�̃t�@�C���ւ̕ۑ��A�����A
# MNIST�g���[�j���O�f�[�^�t�@�C���ւ̓ǂݏ����A������
# Chainer���f���N���X�̕ۑ��A�������Ǘ����郊�\�[�X����N���X
# MNIST/Chainer�����ɂȂ��Ă���̂ŁA�Y���ӏ��������������
# �ق��̋@�B�w�K�ł��g����
class Resource():

    # ���́A�o�̓f�[�^�T�C�Y��`
    # MNIST�ȊO�Ŏg�p�������ꍇ�͏���������

    # ���̓T�C�Y�F8�s�N�Z���~8�s�N�Z���~�P�F(1)�̑S�v�f��
    INPUT_SIZE = 64  # 8 x 8 image size
    # �o�̓T�C�Y�F0����9�܂ł̐����̕��ސ�
    OUTPUT_SIZE = 10  # 10 classification

    # �R���X�g���N�^
    # ���� root: �p�X������i�w��Ȃ���""�j
    # ���e�X�g���ɍ쐬�����e��t�@�C���̐U��o����ς��������߂ɑ��݂���
    #
    # self ��Java��this
    # �R���X�g���N�^����root���w�肳��Ȃ������ꍇ�́A�󕶎��i����j���i�[
    def __init__(self, root=""):
        # __file__ ���s���̃X�N���v�g�t�@�C����\��
        # �R���X�g���N�^����root����̏ꍇ
        # resource.py�̂���f�B���N�g�� + "./store" ���A
        # �����łȂ��ꍇ�̓R���X�g���N�^���������̂܂܁A
        # �C���X�^���X�ϐ�root�֊i�[
        self.root = root if root else os.path.join(os.path.dirname(__file__), "./store")
        # �C���X�^���X�ϐ�model_path��
        # <resource.py�̂���f�B���N�g��>/store/model ��������
        # <�R���X�g���N�^����root�̎w���f�B���N�g��>/model ���i�[
        self.model_path = os.path.join(self.root, "./model")
        # �C���X�^���X�ϐ� param_file ��
        # <resource.py�̂���f�B���N�g��>/store/params.json ��������
        # <�R���X�g���N�^����root�̎w���f�B���N�g��>/params.jeson ���i�[
        self.param_file = os.path.join(self.root, "./params.json")

    # ���K���p�����[�^��ۑ�
    # ���� means:
    # ���� stds:
    # �߂�l�Ȃ�
    #
    # �����ŗ^����ꂽ�f�[�^��1�s�����񉻂���param_file�֏�������
    def save_normalization_params(self, means, stds):
        # ����ls������to_list�֐����`
        # ls�l��tuple��list�̂ǂ��炩�ł����ls�l���̂܂܂��A
        # �����łȂ����ls�l�����X�g�����ĕԋp����
        to_list = lambda ls: ls if isinstance(ls, (tuple, list)) else ls.tolist()
        # ����params���`
        # ���g�́A���������X�g����������
        params = {
            "means": to_list(means),
            "stds": to_list(stds)
        }
        # JSON�f�[�^��1�s������
        serialized = json.dumps(params)
        # �C���X�^���X�ϐ�param_file�̎w���t�@�C�����o�C�i���������݂ŊJ��
        with open(self.param_file, "wb") as f:
            # params��1�s�����񉻃f�[�^��UTF-8�Ńt�@�C���֏�������
            f.write(serialized.encode("utf-8"))

    # ���K���p�����[�^���t�@�C�����烍�[�h
    # ���� �Ȃ�
    # �߂�l means: ��������means�z��
    # �߂�l stds: ��������stds�z��
    #
    # param_file���w���t�@�C�����J��UTF-8�^���œǂݍ��ݔz��Ƃ��ĕԋp
    def load_normalization_params(self):
        loaded = {}
        if not os.path.isfile(self.param_file):
            raise Exception("Normalization parameter file does not exist.")
        # param_file���w���t�@�C�����@�o�C�i���ǂݍ��ރ��[�h�ŊJ��
        with open(self.param_file, "rb") as f:
            # UTF-8�^���œǂݍ���JSON�f�[�^(����)�Ƃ���loaded�ϐ��֊i�[
            loaded = json.loads(f.read().decode("utf-8"))
        # �����l��z�񉻂���֐����`
        to_array = lambda x: np.array([float(_x) for _x in x], dtype=np.float32)
        # means�̕����l�z��Astds�̕����l�z���ԋp
        return to_array(loaded["means"]), to_array(loaded["stds"])
    # �g���[�j���O�f�[�^�����[�h
    # �����Ȃ�
    # �߂�l x: ���������g���[�j���O�f�[�^��input
    # �߂�l y: ���������g���[�j���O�f�[�^��output
    #
    # �g���[�j���O�f�[�^��ǂݍ��݁A�߂�l�Ƃ��ĕԋp����
    # �{�R�[�h���R�s�y�ŗ��p����ꍇ�͂��̊֐������������A
    # ���[�J���t�@�C����̃t�@�C����ǂݍ��݁A�߂�l����������ɕύX����
    def load_training_data(self):
        # scikit-learn�ɗp�ӂ���Ă���MNIST�f�[�^���g�p
        from sklearn.datasets import load_digits
        # predifine set is from scikit-learn dataset
        # http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html

        digits = load_digits()
        x = digits.data
        y = digits.target

        return x, y

    # �f�[�^��ۑ�����
    # ���� path: �ۑ���t�@�C���̃p�X
    # ���� data: �ۑ��Ώۂ̃f�[�^�i0�ԖځF���x���A1�Ԗڈȍ~�F���������_���j
    #
    # ����data������path���w���t�@�C���֒ǉ��������݂���
    def save_data(self, path, data):
        # ����path�̎w���t�@�C����ǉ��������݃o�C�i�����[�h�ŊJ��
        with open(path, "ab") as f:
            # data[0]��int������label�ϐ���
            # data[1,2,...]��float������features�z���
            label = int(data[0])
            features = [float(d) for d in data[1:]]
            # features�z�񒷂�INPUT_SIZE���傫���ꍇ
            if len(features) > self.INPUT_SIZE:
                # data_processor.py���DataProcessor�N���X�𐶐�
                dp = DataProcessor()
                # INPUT_SIZE���̔z��ɒ�������freatures�z��֊i�[
                features = dp.adjust(np.array([features]), self.INPUT_SIZE).tolist()[0]
            # features�z�񒷂�INPUT_SIZE��菬�����ꍇ
            elif len(features) < self.INPUT_SIZE:
                # ��O�𔭐�
                raise Exception("Size mismatch when saving the data.")
            # ���x���Afeatures�z����^�u�ŃZ�p���[�g����������{���s
            line = "\t".join([str(e) for e in [label] + features]) + "\n"
            # UTF-8�^���ŕۑ�
            f.write(line.encode("utf-8"))

    # �f�[�^�����[�h����
    # ���� path: �ۑ���t�@�C���̃p�X
    # �߂�l x: np.ndarray�^���̔z��ifeature�z��l�j
    # �߂�l y: np.ndarray�^���̔z��ilabel�l��v�f1�̔z�񉻂������́j
    #
    # ����path���w���t�@�C������ǂݍ��݁A
    # np.ndarray�^���̕��������_�z�񉻂��ĕԋp����
    def load_data(self, path):
        x = []
        y = []
        with open(path, mode="r", encoding="utf-8") as f:
            for line in f:
                # ���s���܂߂��󔒕����𗼒[���珜��
                line = line.strip()
                # read_data�֐����Ăяo���Alabel(�ŏ��̗v�f)�A
                # features�z��(2�Ԃ߈ȍ~�̗v�f��z��)������
                label, features = self.read_data(line)
                # features�z��
                x.append(features)
                # �ϐ�y��v�f�P�̔z��ɂ���label�l��ۑ�
                y.append(label)
        # np.ndarrya�^���̔z��ɕς��āA�ԋp
        x = np.array(x, dtype=np.float32)
        y = np.array(y, dtype=np.float32)
        return x, y

    # TSV�^���P�s����������x����features�z��ɐ؂�o��
    # ���� line: �����Ώۂ̕�����i�P�s��\��������A���s�Ȃ��j
    def read_data(self, line):
        # �^�u�Ő؂�o��
        elements = line.split("\t")
        # �ŏ��̗v�f����int�����ă��x����
        label = int(elements[0])
        # �̂����float�����Ĕz�񉻂����x���ƈꏏ�ɕԋp
        features = [float(e) for e in elements[1:]]
        return label, features

    # ���f����ۑ�����
    # ���� model:
    # �߂�l�Ȃ�
    #
    # �C���X�^���X�ϐ�model_path���w���f�B���N�g���̉���
    # <���������������f���̃N���X��>_<YYYYmmddHHMMSS�^���̌��ݓ��t>.model ��
    # �����t�@�C�����ŕۑ�����
    # chainer���C�u�������g���Ă���̂ŕʂ̃��C�u�������g�p����ꍇ�͏���������
    # �K�v������
    def save_model(self, model):
        # �C���X�^���X�ϐ�model_path���w���f�B���N�g�������݂��Ȃ��ꍇ
        if not os.path.exists(self.model_path):
            # �f�B���N�g�����쐬����
            os.mkdir(self.model_path)
        # �t�@�C����
        # <���������������f���̃N���X��>_<YYYYmmddHHMMSS�^���̌��ݓ��t>.model 
        # �̐擪�Ƀf�B���N�g���p�X��}��
        timestamp = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        model_file = os.path.join(self.model_path, "./" + model.__class__.__name__.lower() + "_" + timestamp + ".model")
        # chainer���C�u�����̕ۑ��֐��������ĕۑ�����
        serializers.save_npz(model_file, model)

    # ���f�������[�h����
    # ���� model: model�N���X�C���X�^���X(chainer.Chain�T�u�N���X)
    # �߂�l�Ȃ�
    #
    # �C���X�^���X�ϐ�model_path���w���f�B���N�g���̉��̍ŐV�̃t�@�C����
    # �g���Ĉ���model�̏�Ԃ𕜌�����
    # chainer���C�u�������g���Ă���̂ŕʂ̃��C�u�������g�p����ꍇ�͏���������
    # �K�v������
    def load_model(self, model):
        # �C���X�^���X�ϐ� model_path �̎w���f�B���N�g�������݂��Ȃ��ꍇ
        if not os.path.exists(self.model_path):
            # ��O�𔭐�
            raise Exception("model file directory does not exist.")

        # model_path ���� <���f���N���X���̏�������>*.model �Ƃ����t�@�C��
        # �̂Ȃ��ōł��������ŐV�̃t�@�C�����������ϐ�model_file�֊i�[
        suffix = ".model"
        keyword = model.__class__.__name__.lower()
        candidates = []
        for f in os.listdir(self.model_path):
            if keyword in f and f.endswith(suffix):
                candidates.append(f)
        candidates.sort()
        latest = candidates[-1]
        #print("targets {}, pick up {}.".format(candidates, latest))
        model_file = os.path.join(self.model_path, latest)
        # chainer���C�u�����̃��[�h�֐����g���ď�Ԃ𕜌�����
        serializers.load_npz(model_file, model)
