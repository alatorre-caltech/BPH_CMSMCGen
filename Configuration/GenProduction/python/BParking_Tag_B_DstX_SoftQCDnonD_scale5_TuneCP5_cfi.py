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
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring(
                'Myanti-B0',
                'MyB0',
                'MyB+',
                'MyB-'
            ),
            operates_on_particles = cms.vint32(511, 521),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyD0              D0
Alias      Myanti-D0         anti-D0
Alias      MyD*-             D*-
Alias      MyD*+             D*+
Alias      MyB0              B0
Alias      Myanti-B0         anti-B0
Alias      MyB+              B+
Alias      MyB-              B-

ChargeConj MyD0             Myanti-D0
ChargeConj MyD*-            MyD*+
ChargeConj MyB0             Myanti-B0
ChargeConj MyB+             MyB-

Decay MyD0
1.000       K-  pi+           PHSP;
Enddecay
CDecay Myanti-D0

Decay MyD*-
1.000       Myanti-D0 pi-     VSS;
Enddecay
CDecay MyD*+

Decay MyB0
0.0493   MyD*-    e+      nu_e                  PHOTOS HQET2 1.207 0.920 1.406 0.853; #
0.0150   MyD*-    pi+     pi0                   PHSP; # 50
0.0072   MyD*-    pi+     pi+     pi-           PHSP; # 57
0.0130   MyD*-    a_1+                          SVV_HELAMP 0.200 0.0 0.866 0.0 0.458 0.0; # 60
0.0176   MyD*-    pi+     pi+     pi-    pi0    PHSP; # 63
Enddecay
CDecay Myanti-B0

Decay MyB+
0.0150   MyD*-    pi+     pi+     pi0           PHSP; # 143
0.0026   MyD*-    pi+     pi+     pi+    pi-    PHSP; # 144
Enddecay
CDecay MyB-

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

D0filter = cms.EDFilter(
    "PythiaDauVFilter",
    ChargeConjugation  = cms.untracked.bool(True),
    ParticleID         = cms.untracked.int32(-421),
    MotherID           = cms.untracked.int32(-413),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(321, -211),
    MinPt              = cms.untracked.vdouble(0.3, 0.3),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)


ProductionFilterSequence = cms.Sequence(generator + D0filter)
