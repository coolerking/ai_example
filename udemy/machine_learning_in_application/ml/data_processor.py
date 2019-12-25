# coding: -*- utf-8 -*-
import numpy as np

# �f�[�^�����N���X
#
# �f�[�^�������[�e�B���e�B�Ƃ��Ďg�p�����
# �C���X�^���X�ϐ� means: ���̓f�[�^�̕��ϒl
# �C���X�^���X�Ր� stds: ���̓f�[�^�̕W���΍�
class DataProcessor():

    # �R���X�g���N�^�����̊֐�
    # ���� means: �f�t�H���g��̃^�v���i�㏑���ł��Ȃ����X�g�̗l�Ȃ��́j
    # ���� stds: �f�t�H���g��̃^�v��
    #
    # �e�����l���C���X�^���X�ϐ��Q�֊i�[����
    def __init__(self, means=(), stds=()):
        self.means = means
        self.stds = stds

    # ���̓f�[�^�t�H�[�}�b�g�֐�
    # ���� x: ���̓f�[�^
    # ���� size: �v�[�����O��̎������A�f�t�H���g-1
    #
    # �v�[�����O�����������Ameans�l��������stds�l�Ŋ������l��ԋp����
    # size�l�� 0�ȉ��̏ꍇ�Ȃǂ̓v�[�����O�����������Ȃ�
    def format_x(self, x, size=-1):
        # ���������[�J���ϐ�_x�Ŏ󂯎��
        _x = x
        # x ���^�v�������X�g�ł���ꍇ
        if isinstance(x, (tuple, list)):
            # np.npdarray�^���֕ϊ���_x�֊i�[
            _x = np.array([x])
        # ����size��������_x �̂Q�Ԃ߂̗v�f�̎�����size�l�ƈႤ�ꍇ
        if size > 0 and _x.shape[1] != size:
            # ����x�ɑ΂��ăv�[���������ɂ�钲�������������ʂ�_x��
            _x = self.adjust(x, size)
        # �v�f�����ׂ�float32�^�ɕϊ�
        _x = _x.astype(np.float32, copy=False)

        # �C���X�^���X�ϐ�means�̒����A�C���X�^���X�ϐ�stds�̒������Ƃ���
        # 0���傫���ꍇ
        if len(self.means) > 0 and len(self.stds) > 0:
            # _x����means������stds�Ŋ������l(float32)��ԋp
            return (_x - self.means) / self.stds
        # �C���X�^���X�ϐ�means�̒����A�C���X�^���X�ϐ�stds�̒����̂ǂ��炩��
        # 0�ȉ��̏ꍇ
        else:
            # _x�����̂܂ܕԋp
            return _x

    # ���̓f�[�^�̒������s���֐�
    # ���� x: ���̓f�[�^
    # ���� size: �e���̓f�[�^�̎�����
    # �߂�l x: �����ςݓ��̓f�[�^
    #
    # �����ŗ^����ꂽ���̓f�[�^�̎�����size�l�ɒ������ĕԋp����
    def adjust(self, x, size):
        # �֐����֐� max_pooling
        # ���� v:�A�E�g�v�b�g
        # �߂�l: np.ndarray�^���A�v�[�����O������̃A�E�g�v�b�g
        #
        # ���X�g��̕ϐ�v�ɑ΂��ăv�[�����O����(kmax pooling)�������ԋp����
        def max_pooling(v):
            # �֐� sqrt(_x)��lambda���Œ�`
            # ���� _x: ���X�g���C�N�ȕϐ�
            # �߂�l: _x�̊e�v�f�̕������̏�������l����������
            sqrt = lambda _x: int(np.ceil(np.sqrt(_x)))
            # size�l����L��sqrt�֐��ŕ�����������
            _target_square_size = sqrt(size)
            # ����v�̒����̕���������Lsqrt�֐��Ŏ擾
            square_size = sqrt(len(v))
            # ����v�̕����� �� �e�֐��̈���size�̕������Ő؂�̂Ċ���Z(int)
            conv_size = int(square_size // _target_square_size)
            # ����v�̒l���A����v�̒����̕������~����v�̒����̕����� �̍s��
            image = np.reshape(v, (square_size, square_size))
            # ���[�J���ϐ� _pooled ����̃��X�g�ŏ�����
            _pooled = []
            # i��0����size-1�܂Ń��[�v
            # conv_size�~conv_size�̃E�B���h�E��max pooling�������A���ʂ�
            # ���X�g _pooled �֊i�[
            # ������v�ɑ΂��ăv�[�����O�w�̏��������s���A���ʃ��X�g���쐬����
            for i in range(size):
                # �ϐ�row:
                # 0, 0,..(_target_square_size��).., 0, 
                # conv_size, conv_size, ..(_target_square_size��).., conv_size,
                # conv_size*2, conv_size*2, ..
                # (_target_square_size��).., conv_size*size/_target_square_size
                # �ϐ�col:
                # 0,conv_size,conv_size*2,..,conv_size*(_target_square_size-1),
                # 0,conv_size,conv_size*2,..,conv_size*(_target_square_size-1),
                # ..
                row, col = int(i // _target_square_size * conv_size), int(i % _target_square_size * conv_size)
                # conv_size�~conv_size�̃E�B���h�E�ōő�̗v�f�l��ϐ�mp��
                mp = np.max(image[row:row + conv_size, col: col + conv_size])
                # _poooled ���X�g�̍Ō�̗v�f�Ƃ��Ēǉ�
                _pooled.append(mp)
            # max_pooling�������ʂ�ԋp
            return np.array(_pooled)
        # ����x����L��max pooling�֐����g���ăv�[�����O�����ɂ����ԋp����
        x = np.array([max_pooling(_v) for _v in x])
        return x

    # �o�̓f�[�^��v�f��int32�ŗv�f��1��np.ndarray�^�z��ɕϊ�����֐�
    # ���� y: �o�̓f�[�^
    # �߂�l: �ϊ���np.ndarray�^�z��
    def format_y(self, y):
        _y = y
        # ����y��int�̏ꍇ
        if isinstance(y , int):
            # �v�f���P��np.ndarry�z��
            _y = np.array([y])
        # _y�̗v�f��int32�^�ɕϊ�
        _y = _y.astype(np.int32, copy=False)
        # �v�f��int32�ŗv�f��1��np.ndarray�^�z��ɕϊ����ĕԋp
        return _y 

    # ���K���p�����[�^���C���X�^���X�ϐ��Q�ɃZ�b�g����֐�
    # ���� x: ���̓f�[�^
    # �߂�l�Ȃ�(�C���X�^���X�ϐ�means�Astds�X�V)
    #
    # �C���X�^���X�ϐ�means��stds�𐳋K���p�����[�^�l���Z�b�g�X��
    def set_normalization_params(self, x):
        # np.means�֐�: ���ϒl�����߂�(averge�ƈ���ďd�ݕt���Ή����Ă��Ȃ�)
        # x: �z�񃉃C�N�ȕϐ��A���ϒl�����߂�ΏۂƂȂ�
        # axis: ���A�ǂ̎��ɉ����ĕ��ς����߂邩
        # dtype: ���ς����߂�ۂɎg�p����f�[�^�^
        # �ԋp�l: x�v�f��(axis�����Ƃ���)���ϒl��dtype�Ŏw�肵���^�ŕԋp

        # �C���X�^���X�ϐ��lmeans
        # �� x�̑S�v�f�̕��ς�0�����Ƃ���float32�^���ŋ��߂�
        self.means = np.mean(x, axis=0, dtype=np.float32)

        # np.std�֐�: �W���΍������߂�
        # x: �z�񃉃C�N�ȕϐ��A�W���΍������߂�ΏۂƂȂ�
        # axis: ���A�ǂ̎��ɉ����ĕ��ς����߂邩
        # dtype: �W���΍������߂�ۂɎg�p����f�[�^�^
        # �ԋp�l: x�v�f��(axis�����Ƃ���)�W���΍���dtype�Ŏw�肵���^�ŕԋp

        # �C���X�^���X�ϐ��l stds
        # �� x�̑S�v�f��0�����Ƃ����W���΍���float32�^���ŋ��߂�
        self.stds = np.std(x, axis=0, dtype=np.float32)

        # simple trick to avoid 0 divide
        # 0�Ŋ��邱�Ƃ������ȒP�ȃg���b�N

        # stds�l��1.0e-6���傫���ꍇ�͍ŏ��̗v�f�ɁA
        # stds�l��1.0e-6�����̏ꍇ��2�Ԃ߂̗v�f�ɁA
        # x�̍ő�l����ŏ��l���i�[
        self.stds[self.stds < 1.0e-6] = np.max(x) - np.min(x)
        # means�l��1.0e-6���傫���ꍇ�͍ŏ��̗v�f�ɁA
        # means�l��1.0e-6�����̏ꍇ��2�Ԃ߂̗v�f�ɁA
        # x�̍ŏ��l���i�[
        self.means[self.stds < 1.0e-6] = np.min(x)

    # �o�b�`�C�e���[�^
    # ���� X: ���̓f�[�^
    # ���� y: �o�̓f�[�^(�����f�[�^)
    # ���� batch_size: �o�b�`�T�C�Y
    # ���� epoch: �o�b�`�񐔁A�f�t�H���g1��
    # �߂�l x_batch: �o�b�`1�񕪂̓��̓f�[�^
    # �߂�l y_batch: �o�b�`1�񕪂̏o�̓f�[�^�i�����f�[�^�j
    # �߂�l epoch_end: epoch �̏I��肩�ǂ����̐^�U�l
    def batch_iter(self, X, y, batch_size, epoch=1):
        # np.ndarray�z�� [0, 1, 2,.., (�o�̓f�[�^�̗v�f��-1)]
        indices = np.array(range(len(y)))
        # batch_size ���� �o�̓f�[�^�v�f����bacht_size�Ŋ��������܂�ň�������
        appendix = batch_size - len(y) % batch_size
        # e �� 0, 1, .., (�o�̓f�[�^�̗v�f��-1)
        for e in range(epoch):
            # np.ndarray�z�� [0, 1,.. (�o�̓f�[�^�̗v�f��-1)]�̗v�f���V���b�t��
            np.random.shuffle(indices)
            # �V���b�t���ς݂̔z���
            # �V���b�t���ς݂̔z��(�v�f�擪����appendix���܂�)��A����������
            batch_indices = np.concatenate([indices, indices[:appendix]])
            # batch_size��(�o�̓f�[�^�̗v�f��+appendix)��batch_size��
            # �؂�̂ď��Z
            # �o�b�`����
            batch_count = len(batch_indices) // batch_size
            # b �� 0, 1, ..  , �o�b�`����-1
            for b in range(batch_count):
                # b+1��ڂ̃o�b�`�f�[�^��؂�o���A���́E�o�̓f�[�^�̗v�f�ʒu��
                # batch_indices������o��
                elements = batch_indices[b * batch_size:(b + 1) * batch_size]
                # �v�f�ʒuelement���o�b�`1�����f�[�^�Ƃ��Đ؂�o��
                x_batch = X[elements]
                y_batch = y[elements]
                # b �̒l���Ō�̏ꍇ True�A�����ł͂Ȃ��ꍇ False
                epoch_end = True if b == batch_count - 1 else False
                # ���̒i�K�Ŗ߂�l��Ԃ�
                # ����Ăяo�����ꍇ�́A���̍s�̎��ifor b..�̎��� for e..�̎�)
                # �����s����ipython��yield�@�\�j
                yield x_batch, y_batch, epoch_end
