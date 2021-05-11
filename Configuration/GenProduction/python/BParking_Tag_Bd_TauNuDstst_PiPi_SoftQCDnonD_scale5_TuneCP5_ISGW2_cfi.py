import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('customDecayFiles/evt_voc1.pdl'),
            list_forced_decays = cms.vstring(
                'Myanti-B0',
                'MyB0',
            ),
            operates_on_particles = cms.vint32(511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyTau+      tau+
Alias      MyTau-      tau-
Alias      MyD0        D0
Alias      Myanti-D0   anti-D0
Alias      MyD*-       D*-
Alias      MyD*+       D*+
Alias      MyD*(2S)-   D*(2S)-
Alias      MyD*(2S)+   D*(2S)+
Alias      MyB0        B0
Alias      Myanti-B0   anti-B0

ChargeConj MyTau+     MyTau-
ChargeConj MyD0       Myanti-D0
ChargeConj MyD*-      MyD*+
ChargeConj MyD*(2S)-  MyD*(2S)+
ChargeConj MyB0       Myanti-B0

Decay MyTau+
1.000      mu+  nu_mu   anti-nu_tau         TAULNUNU;
Enddecay
CDecay MyTau-

Decay MyD0
1.000       K-  pi+           PHSP;
Enddecay
CDecay Myanti-D0

Decay MyD*-
1.000       Myanti-D0 pi-     VSS;
Enddecay
CDecay MyD*+

Decay MyD*(2S)-
0.80    MyD*- pi+ pi-                     PHSP;
0.20    MyD*- pi0 pi0                     PHSP;
Enddecay
CDecay MyD*(2S)+


Decay MyB0
1.00   MyD*(2S)-   MyTau+  nu_mu      PHOTOS   ISGW2;
Enddecay
CDecay Myanti-B0

End
"""
            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on',
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 5.0',
#             'PTFilter:quarkPt = 3',
#             'PTFilter:quarkRapidity = 3',
		),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########

tau_mufilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(-15),  ## Tau
    MotherID           = cms.untracked.int32(511),  ## B0
    ChargeConjugation  = cms.untracked.bool(True),
    NumberDaughters    = cms.untracked.int32(3),
    DaughterIDs        = cms.untracked.vint32(-16, -13, 14),
    MinPt              = cms.untracked.vdouble(-1., 6.7, -1.),
    MinEta             = cms.untracked.vdouble(-9999999., -1.6, -9999999.),
    MaxEta             = cms.untracked.vdouble( 9999999.,  1.6, 9999999.)
)


ProductionFilterSequence = cms.Sequence(generator + tau_mufilter)
