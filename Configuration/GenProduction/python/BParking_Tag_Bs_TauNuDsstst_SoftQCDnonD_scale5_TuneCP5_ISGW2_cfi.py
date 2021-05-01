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
                'MyB_s0',
                'Myanti-B_s0'
            ),
            operates_on_particles = cms.vint32(531),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyTau+      tau+
Alias      MyTau-      tau-
Alias      MyD0        D0
Alias      Myanti-D0   anti-D0
Alias      MyD*-       D*-
Alias      MyD*+       D*+
Alias      MyD'_s1-     D'_s1-
Alias      MyD'_s1+     D'_s1+
Alias      MyD_s2*-    D_s2*-
Alias      MyD_s2*+    D_s2*+
Alias      MyB_s0      B_s0
Alias      Myanti-B_s0 anti-B_s0

ChargeConj MyTau+   MyTau-
ChargeConj MyD0     Myanti-D0
ChargeConj MyD*-    MyD*+
ChargeConj MyD'_s1-  MyD'_s1+
ChargeConj MyD_s2*- MyD_s2*+
ChargeConj MyB_s0   Myanti-B_s0

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

Decay MyD'_s1-
1.000       MyD*- anti-K0        VVS_PWAVE  0.0 0.0 0.0 0.0 1.0 0.0;
Enddecay
CDecay MyD'_s1+

Decay MyD_s2*-
1.000       MyD*- anti-K0        TVS_PWAVE  0.0 0.0 1.0 0.0 0.0 0.0;
Enddecay
CDecay MyD_s2*-

Decay MyB_s0
0.0027   MyD'_s1-   MyTau+    nu_tau  PHOTOS  ISGW2;
0.0005   MyD_s2*-   MyTau+    nu_tau  PHOTOS  ISGW2;
Enddecay
CDecay Myanti-B_s0

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
    MotherID           = cms.untracked.int32(531),  ## B_s0
    ChargeConjugation  = cms.untracked.bool(True),
    NumberDaughters    = cms.untracked.int32(3),
    DaughterIDs        = cms.untracked.vint32(-16, -13, 14),
    MinPt              = cms.untracked.vdouble(-1., 6.7, -1.),
    MinEta             = cms.untracked.vdouble(-9999999., -1.6, -9999999.),
    MaxEta             = cms.untracked.vdouble( 9999999.,  1.6, 9999999.)
)


ProductionFilterSequence = cms.Sequence(generator + tau_mufilter)
