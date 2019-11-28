"""Run Alleyoop utrrates tool on Slamdunk results."""
import os

from plumbum import TEE

from resolwe.process import Cmd, DataField, FileField, Process, StringField


class AlleyoopUtrRates(Process):
    """Run Alleyoop utrrates."""

    slug = 'alleyoop-utr-rates'
    process_type = 'data:alleyoop:utrrates'
    name = 'Alleyoop UTR Rates'
    requirements = {
        'expression-engine': 'jinja',
        'executor': {
            'docker': {
                'image': 'resolwebio/slamdunk:1.0.0'
            },
        },
        'resources': {
            'cores': 1,
            'memory': 16384,
        },
    }
    entity = {
        'type': 'sample',
    }
    category = 'Slamdunk'
    data_name = '{{ slamdunk|sample_name|default("?") }}'
    version = '1.0.0'

    class Input:
        """Input fields for AlleyoopUtrRates."""

        ref_seq = DataField('seq:nucleotide', label='FASTA file containig sequences for aligning')
        regions = DataField('bed', label='BED file with coordinates of regions of interest')
        slamdunk = DataField('alignment:bam:slamdunk', label='Slamdunk results')

    class Output:
        """Output fields to process AlleyoopUtrRates."""

        report = FileField(label='Tab-separated file containing conversion rates on each region of interest')
        plot = FileField(label='Region of interest conversion rate plot')
        species = StringField(label='Species')
        build = StringField(label='Build')

    def run(self, inputs, outputs):
        """Run analysis."""
        basename = os.path.basename(inputs.slamdunk.bam.path)
        assert basename.endswith('.bam')
        name = basename[:-4]
        args = [
            '-o', 'utrrates',
            '-r', inputs.ref_seq.fasta.path,
            '-b', inputs.regions.bed.path,
        ]

        return_code, _, _ = Cmd['alleyoop']['utrrates'][args][inputs.slamdunk.bam.path] & TEE(retcode=None)
        if return_code:
            self.error('Alleyoop utrrates analysis failed.')

        rates_file = os.path.join('utrrates', f'{name}_mutationrates_utr.csv')
        rates_file_renamed = os.path.join('utrrates', f'{name}_mutationrates.txt')
        os.rename(rates_file, rates_file_renamed)

        outputs.report = rates_file_renamed
        outputs.plot = os.path.join('utrrates', f'{name}_mutationrates_utr.pdf')
        outputs.species = inputs.slamdunk.species
        outputs.build = inputs.slamdunk.build
