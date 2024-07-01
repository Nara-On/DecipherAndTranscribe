"""Experiment with an RNN-based Seq2Seq model."""

#--config_path configs/exp_seq2seq/exp_seq2seq_1.json
from pathlib import Path

from seq_recog.data.base_dataset import BaseVocab, BaseDataset, BaseDataConfig
from seq_recog.experiments.base_experiment import Experiment, ExperimentConfig
from seq_recog.experiments.configurations import Seq2SeqDirectoryConfig
from seq_recog.formatters import seq2seq_formatters
from seq_recog.loggers.base_logger import SimpleLogger
from seq_recog.metrics import text
from seq_recog.models.rnn_seq2seq import KangSeq2Seq, KangSeq2SeqConfig
from seq_recog.trainers.base_trainer import BaseTrainer, BaseTrainerConfig
from seq_recog.validators.base_validator import BaseValidator


class Seq2SeqExperimentConfig(ExperimentConfig):
    """Global experiment settings."""

    dirs: Seq2SeqDirectoryConfig
    data: BaseDataConfig
    model: KangSeq2SeqConfig
    train: BaseTrainerConfig


class Seq2SeqExperiment(Experiment):
    """Object modelling the Experiment with Arnau Baró's CRNN model."""

    EXPERIMENT_CONFIG = Seq2SeqExperimentConfig

    def __init__(self):
        """Initialise object."""
        super().__init__()

    def initialise_everything(self) -> None:
        """Initialise all member variables for the class."""
        # Data
        self.vocab = BaseVocab(self.cfg.dirs.vocab_data)

        self.train_data = BaseDataset(
            self.cfg.dirs.training_root,
            self.cfg.dirs.training_file,
            self.vocab,
            self.cfg.data,
            True,
        )
        self.valid_data = BaseDataset(
            self.cfg.dirs.validation_root,
            self.cfg.dirs.validation_file,
            self.vocab,
            self.cfg.data,
            False,
        )
        self.test_data = BaseDataset(
            self.cfg.dirs.test_root,
            self.cfg.dirs.test_file,
            self.vocab,
            self.cfg.data,
            False,
        )
        
        # Formatters
        self.training_formatter = seq2seq_formatters.GreedyTextDecoder()
        self.valid_formatter = seq2seq_formatters.GreedyTextDecoder()

        # Metrics Transcription
        self.training_metric = text.Levenshtein(self.vocab)
        self.valid_metric = text.Levenshtein(self.vocab)        
        
        #self.training_metric = text.CharErrorRate(self.vocab)
        #self.valid_metric = text.CharErrorRate(self.vocab)

        # Model and training-related
        self.model = KangSeq2Seq(self.cfg.model, self.cfg.data)
        self.validator = BaseValidator(
            self.valid_data,
            self.valid_formatter,
            self.valid_metric,
            Path(self.cfg.dirs.results_dir),
            self.cfg.train.batch_size,
            0 if self.debug else self.cfg.train.workers,
            "valid",
            SimpleLogger,
        )
        self.tester = BaseValidator(
            self.test_data,
            self.valid_formatter,
            self.valid_metric,
            Path(self.cfg.dirs.results_dir),
            self.cfg.train.batch_size,
            0 if self.debug else self.cfg.train.workers,
            "test",
            SimpleLogger,
        )

        self.trainer = BaseTrainer(
            self.model,
            self.train_data,
            self.cfg.train,
            Path(self.cfg.dirs.results_dir),
            self.validator,
            self.training_formatter,
            self.training_metric,
            None,
            SimpleLogger,
        )


if __name__ == "__main__":
    exp = Seq2SeqExperiment()
    exp.main()
