# coding: -*- utf-8 -*-
import chainer
import chainer.functions as F
import chainer.links as L

# NumberRecognizeNN(���l���ʃj���[�����l�b�g���[�N)�N���X
# �֐����ۂ����s����ƃ��f����ʂ����ƂɂȂ�悤�Ɏ�������
# Chainer�Ǝ������œ����Ă��邽�߁A�ʂ̃��C�u�������g�p����ꍇ
# ���g�͂قڏ��������ƂȂ�
class NumberRecognizeNN(chainer.Chain):

    # �C���X�^���X���������������i�R���X�g���N�^�����j
    # ���� input_size: ���̓f�[�^�x�N�g��������(�摜�f�[�^���s�N�Z����)
    # ���� output_size: �o�̓f�[�^�x�N�g��������(�v�f��)
    # ���� hidden_size: �B��w�̓��o�̓T�C�Y�A�f�t�H���g200
    # ���� layer_size: �w���A�f�t�H���g3
    def __init__(self, input_size, output_size, hidden_size=200, layer_size=3):
        # ���ׂĂ̈������C���X�^���X�ϐ��֊i�[
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.layer_size = layer_size
        # �e�N���Xchainer.Chain��__init()__�����s����
        # �����Ɋe�w�̒�`
        # L.Liner �S�����w�F�אڂ����̃��j�b�g���m���S��������K^n_n�O���t���
        # �w�A�d�݂�o�C�A�X��Linear�C���X�^���X�����ڕێ�
        super(NumberRecognizeNN, self).__init__(
            l1=L.Linear(self.input_size, hidden_size),
            l2=L.Linear(hidden_size, hidden_size),
            l3=L.Linear(hidden_size, self.output_size),
        )

    # NumberRecognizeNN �����s����
    # ���� x: ���̓f�[�^
    # �߂�l o: �o�̓f�[�^�i�\���f�[�^�j
    #
    # ���̓f�[�^�ɑ΂��A
    # ���`�p�[�Z�v�g������ReLU�����`�p�[�Z�v�g������ReLU�����`�p�[�Z�v�g����
    # ��sigmoid �����������ʂ�\���f�[�^�Ƃ��ĕԂ�
    def __call__(self, x):
        # �e�w�̌��ʂɊ������֐����Ō�Ɏ��s
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        o = F.sigmoid(self.l3(h2))
        return o
