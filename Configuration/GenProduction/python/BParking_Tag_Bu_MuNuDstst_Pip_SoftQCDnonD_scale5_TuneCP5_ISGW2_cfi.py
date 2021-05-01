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
                'MyB+',
                'MyB-',
            ),
            operates_on_particles = cms.vint32(521),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyD0          D0
Alias      Myanti-D0     anti-D0
Alias      MyD*-         D*-
Alias      MyD*+         D*+
Alias      MyD_10        D_10
Alias      Myanti-D_10   anti-D_10
Alias      MyD'_10       D'_10
Alias      Myanti-D'_10  anti-D'_10
Alias      MyD_2*0       D_2*0
Alias      Myanti-D_2*0  anti-D_2*0
Alias      MyB+          B+
Alias      MyB-          B-

ChargeConj MyD0     Myanti-D0
ChargeConj MyD*-    MyD*+
ChargeConj MyD_10   Myanti-D_10
ChargeConj MyD'_10  Myanti-D'_10
ChargeConj MyD_2*0  Myanti-D_2*0
ChargeConj MyB+     MyB-

Decay MyD0
1.000       K-  pi+           PHSP;
Enddecay
CDecay Myanti-D0

Decay MyD*-
1.000       Myanti-D0 pi-     VSS;
Enddecay
CDecay MyD*+

Decay MyD_10
1.000    MyD*+ pi-                        VVS_PWAVE  0.0 0.0 0.0 0.0 1.0 0.0;
Enddecay
CDecay Myanti-D_10

Decay MyD'_10
1.000    MyD*+ pi-                        VVS_PWAVE  1.0 0.0 0.0 0.0 0.0 0.0;
Enddecay
CDecay Myanti-D'_10

Decay MyD_2*0
1.000    MyD*+ pi-                        TVS_PWAVE  0.0 0.0 1.0 0.0 0.0 0.0;
Enddecay
CDecay Myanti-D_2*0

# Resonances relative contribution from B+ -> D* pi munu. Divide the numbers below by 2 (isospin) to get the excted branching fraction.
Decay MyB+
0.00303   Myanti-D_10    mu+    nu_mu  PHOTOS  ISGW2;
0.00270   Myanti-D'_10   mu+    nu_mu  PHOTOS  ISGW2;
0.00101   Myanti-D_2*0   mu+    nu_mu  PHOTOS  ISGW2;
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

tagfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13), ## mu
    MotherID = cms.untracked.int32(521) ## B+
)


ProductionFilterSequence = cms.Sequence(generator + tagfilter)
