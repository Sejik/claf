
import logging

from overrides import overrides

from claf.data.reader import SeqClsBertReader
from claf.decorator import register

logger = logging.getLogger(__name__)


@register("reader:cola_bert")
class CoLABertReader(SeqClsBertReader):
    """
    CoLA DataReader for BERT

    * Args:
        file_paths: .tsv file paths (train and dev)
        tokenizers: defined tokenizers config
    """

    CLS_TOKEN = "[CLS]"
    SEP_TOKEN = "[SEP]"
    UNK_TOKEN = "[UNK]"

    CLASS_DATA = [0, 1]

    def __init__(
        self,
        file_paths,
        tokenizers,
        sequence_max_length=None,
        is_test=False,
    ):

        super(CoLABertReader, self).__init__(
            file_paths,
            tokenizers,
            sequence_max_length,
            class_key=None,
            is_test=is_test,
        )

    @overrides
    def _get_data(self, file_path, **kwargs):
        data_type = kwargs["data_type"]

        _file = self.data_handler.read(file_path)
        lines = _file.split("\n")

        data = []
        for i, line in enumerate(lines):
            line_tokens = line.split("\t")
            if len(line_tokens) <= 3:
                continue
            data.append({
                "uid": f"{data_type}-{i}",
                "sequence_a": line_tokens[3],
                self.class_key: str(line_tokens[1])
            })

        return data
