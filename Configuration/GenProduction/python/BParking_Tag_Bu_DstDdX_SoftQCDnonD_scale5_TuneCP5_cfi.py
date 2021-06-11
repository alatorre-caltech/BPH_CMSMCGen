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
            operates_on_particles = cms.vint32(511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyLepTau+      tau+
Alias      MyLepTau-      tau-
Alias      MyLepD+        D+
Alias      MyLepD-        D-
Alias      MyLepD*+        D*+
Alias      MyLepD*-        D*-
Alias      MyD0        D0
Alias      Myanti-D0   anti-D0
Alias      MyD*-       D*-
Alias      MyD*+       D*+
Alias      MyB+            B+
Alias      MyB-            B-

ChargeConj MyLepTau+    MyLepTau-
ChargeConj MyLepD+   MyLepD-
ChargeConj MyLepD*+  MyLepD*-
ChargeConj MyD0      Myanti-D0
ChargeConj MyD*-     MyD*+
ChargeConj MyB+     MyB-

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

Decay MyLepD+
0.08760 anti-K0 mu+     nu_mu                           PHOTOS  ISGW2; # PDG
0.05270 anti-K*0 mu+     nu_mu                          PHOTOS  ISGW2; # PDG
0.00350 pi0     mu+     nu_mu                           PHOTOS  ISGW2; # Same as electron
0.00277 anti-K_10 mu+     nu_mu                         PHOTOS  ISGW2; # From PDG electron
0.00100 anti-K_2*0 mu+     nu_mu                        PHOTOS  ISGW2; # From EvtGen
0.00218 rho0    mu+     nu_mu                           PHOTOS  ISGW2; # PDG2014
0.00169 omega   mu+     nu_mu                           PHOTOS  ISGW2; # Same as PDG electron
0.00114 eta     mu+     nu_mu                           PHOTOS  ISGW2; # Same as PDG electron
0.00022 eta'    mu+     nu_mu                           PHOTOS  ISGW2; # Same as PDG electron
0.00063 pi-     pi+     mu+     nu_mu                   PHOTOS  PHSP;  # PDG
0.00190 K-      pi+     mu+     nu_mu                   PHOTOS  PHSP;  # PDG
0.00095 anti-K0 pi0     mu+     nu_mu                   PHOTOS  PHSP;  # PDG
0.00037 mu+     nu_mu                                   PHOTOS  SLN;   # PDG
0.00020 MyLepTau+    nu_tau                             PHOTOS  SLN;   # PDG, includes tau -> mu nunu
Enddecay
CDecay MyLepD-


Decay MyLepD*+
0.3070    MyLepD+  pi0                        VSS;
0.0160    MyLepD+  gamma                      VSP_PWAVE;
Enddecay
CDecay MyLepD*-


Decay MyB+

0.00060   MyD*-    MyLepD+   K+                        PHSP;
0.00030   MyD*-    MyLepD+   K*+                       PHSP;
0.00063   MyLepD-  MyD*+     K+                        PHSP;
0.00031   MyLepD-  MyD*+     K*+                       PHSP;

0.00044  MyD*-    MyLepD*+  K+                        PHSP;
0.00022  MyD*-    MyLepD*+  K*+                       PHSP;

0.00044  MyLepD*- MyD*+     K+                        PHSP;
0.00022  MyLepD*- MyD*+     K*+                       PHSP;

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
    # MotherID = cms.untracked.int32(411) ## D+
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
