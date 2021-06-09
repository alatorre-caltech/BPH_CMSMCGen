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
Alias      MyLepTau+      tau+
Alias      MyLepTau-      tau-
Alias      MyLepD_s+        D_s+
Alias      MyLepD_s-        D_s-
Alias      MyLepD_s*+        D_s*+
Alias      MyLepD_s*-        D_s*-
Alias      MyLepD_s0*+        D_s0*+
Alias      MyLepD_s0*-        D_s0*-
Alias      MyD0        D0
Alias      Myanti-D0   anti-D0
Alias      MyD*-       D*-
Alias      MyD*+       D*+
Alias      MyB_s0      B_s0
Alias      Myanti-B_s0 anti-B_s0

ChargeConj MyLepTau+    MyLepTau-
ChargeConj MyLepD_s+   MyLepD_s-
ChargeConj MyLepD_s*+  MyLepD_s*-
ChargeConj MyLepD_s0*+  MyLepD_s0*-
ChargeConj MyD0      Myanti-D0
ChargeConj MyD*-     MyD*+
ChargeConj MyB_s0   Myanti-B_s0

Decay MyD0
1.000       K-  pi+           PHSP;
Enddecay
CDecay Myanti-D0

Decay MyD*-
1.000       Myanti-D0 pi-     VSS;
Enddecay
CDecay MyD*+

Decay MyLepTau+
1.000      mu+  nu_mu   anti-nu_tau         TAULNUNU;
Enddecay
CDecay MyLepTau-

Decay MyLepD_s+
0.01900 phi     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.02400 eta     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.01100 eta'    mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00340 anti-K0 mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00215 anti-K*0 mu+     nu_mu                          PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00931 MyLepTau+    nu_tau                             PHOTOS  SLN;   # PDG, includes tau -> mu nunu
0.00549 mu+       nu_mu                                 PHOTOS  SLN;   # PDG
Enddecay
CDecay MyLepD_s-


Decay MyLepD_s*+
0.9350 MyLepD_s+    gamma                                   VSP_PWAVE; #[Reconstructed PDG2011]
0.0580 MyLepD_s+    pi0                                     VSS; #[Reconstructed PDG2011]
0.0067 MyLepD_s+    e+         e-                           PHSP; #[Reconstructed PDG2011]
Enddecay
CDecay MyLepD_s*-

Decay MyLepD_s0*+
1.000      MyLepD_s+ pi0                        PHSP;
Enddecay
CDecay MyLepD_s0*-


Decay MyB_s0
0.0150      MyLepD_s*-       MyD*+         K0                     PHSP;
0.0030      MyLepD_s*-       MyD*+         K*0                    PHSP;
0.0050      MyLepD_s-        MyD*+         K0                     PHSP;
0.0025      MyLepD_s-        MyD*+         K*0                    PHSP;
0.0017      MyD*-            MyLepD_s+                            SVS;
0.0017      MyLepD_s*+       MyD*-                                SVV_HELAMP  1.0 0.0 1.0 0.0 1.0 0.0;
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

tagfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13), ## mu
    MotherID = cms.untracked.int32(431) ## D_s+
)

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


ProductionFilterSequence = cms.Sequence(generator + tagfilter + D0filter)
