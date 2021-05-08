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
Alias      MyD0        D0
Alias      Myanti-D0   anti-D0
Alias      MyD*-       D*-
Alias      MyD*+       D*+
Alias      MyD_1-      D_1-
Alias      MyD_1+      D_1+
Alias      MyD'_1-     D'_1-
Alias      MyD'_1+     D'_1+
Alias      MyD_2*-     D_2*-
Alias      MyD_2*+     D_2*+
Alias      MyB0        B0
Alias      Myanti-B0   anti-B0

ChargeConj MyD0     Myanti-D0
ChargeConj MyD*-    MyD*+
ChargeConj MyD_1-   MyD_1+
ChargeConj MyD'_1-  MyD'_1+
ChargeConj MyD_2*-  MyD_2*+
ChargeConj MyB0     Myanti-B0

Decay MyD0
1.000       K-  pi+           PHSP;
Enddecay
CDecay Myanti-D0

Decay MyD*-
1.000       Myanti-D0 pi-     VSS;
Enddecay
CDecay MyD*+

Decay MyD_1-
1.000    MyD*- pi0                        VVS_PWAVE  0.0 0.0 0.0 0.0 1.0 0.0;
Enddecay
CDecay MyD_1+

Decay MyD'_1-
1.000    MyD*- pi0                        VVS_PWAVE  1.0 0.0 0.0 0.0 0.0 0.0;
Enddecay
CDecay MyD'_1+

Decay MyD_2*-
1.000    MyD*- pi0                        TVS_PWAVE  0.0 0.0 1.0 0.0 0.0 0.0;
Enddecay
CDecay MyD_2*+

# Resonances relative contribution from B+ -> D* pi munu. Divide the numbers below by 2 (isospin) to get the excted branching fraction.
Decay MyB0
0.00303   MyD_1-    mu+    nu_mu  PHOTOS  ISGW2;
0.00270   MyD'_1-   mu+    nu_mu  PHOTOS  ISGW2;
0.00101   MyD_2*-   mu+    nu_mu  PHOTOS  ISGW2;
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

tagfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13), ## mu
    MotherID = cms.untracked.int32(511) ## B0
)


ProductionFilterSequence = cms.Sequence(generator + tagfilter)
