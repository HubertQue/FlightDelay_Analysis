import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.nn.init as init
from torch.nn.parameter import Parameter


def save_model(model, iter, name):
    torch.save(model.state_dict(), os.path.join(name, "iter_{}.pth.tar".format(iter)))


def load_model(model, f):
    with open(f, 'rb') as f:
        pretrained_dict = torch.load(f)
        model_dict = model.state_dict()
        pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
        model_dict.update(pretrained_dict)
        model.load_state_dict(model_dict)
    f = str(f)
    if f.find('iter_') != -1 and f.find('.pth') != -1:
        st = f.find('iter_') + 5
        ed = f.find('.pth', st)
        return int(f[st:ed])
    else:
        return 0


class MLPWithSkipConnection(nn.Module):
    def __init__(self, input_size=20, hidden_size1=30, hidden_size2=30, output_size=1):
        super(MLPWithSkipConnection, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size1, hidden_size2)
        self.relu2 = nn.ReLU()
        self.skip_connection = nn.Linear(input_size, hidden_size2)
        self.output_layer = nn.Linear(hidden_size2, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x1 = self.layer1(x)
        x1 = self.relu1(x1)
        x2 = self.layer2(x1)
        x2 = self.relu2(x2)
        # Skip Connection
        skip = self.skip_connection(x)
        combined = x2 + skip
        output = self.output_layer(combined) 
        output = self.sigmoid(output)

        return output


if __name__ == '__main__':
    input_size = 20
    hidden_size1 = 30
    hidden_size2 = 30
    output_size = 1

    model = MLPWithSkipConnection(input_size, hidden_size1, hidden_size2, output_size)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    test_input = torch.randn(1, input_size)

    output = model(sample_input)
    print("Output: ", output)
