import paddle
from paddle import nn


class AttentionLoss(nn.Layer):
    def __init__(self, **kwargs):
        super(AttentionLoss, self).__init__()
        self.loss_func = nn.CrossEntropyLoss(weight=None, reduction='none')

    def forward(self, predicts, batch):
        targets = batch[1].astype("int64")
        label_lengths = batch[2].astype('int64')
        batch_size, num_steps, num_classes = predicts.shape[0], predicts.shape[
            1], predicts.shape[2]
        assert len(targets.shape) == len(list(predicts.shape)) - 1, \
            "The target's shape and inputs's shape is [N, d] and [N, num_steps]"

        inputs = paddle.reshape(predicts, [-1, predicts.shape[-1]])
        targets = paddle.reshape(targets, [-1])

        return {'loss': paddle.sum(self.loss_func(inputs, targets))}
