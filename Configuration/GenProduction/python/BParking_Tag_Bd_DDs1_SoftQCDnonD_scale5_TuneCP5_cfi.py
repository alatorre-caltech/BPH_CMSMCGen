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
            ),
            operates_on_particles = cms.vint32(511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyLepTau+         tau+
Alias      MyLepTau-         tau-
Alias      MyLepD0           D0
Alias      MyLepanti-D0      anti-D0
Alias      MyLepD+           D+
Alias      MyLepD-           D-
Alias      MyLepD*0          D*0
Alias      MyLepanti-D*0     anti-D*0
Alias      MyLepD*+          D*+
Alias      MyLepD*-          D*-
Alias      MyLepD_s+         D_s+
Alias      MyLepD_s-         D_s-
Alias      MyLepD_s*+        D_s*+
Alias      MyLepD_s*-        D_s*-
Alias      MyLepD_s1+        D_s1+
Alias      MyLepD_s1-        D_s1-
Alias      MyLepD_s1_2536-   D'_s1-
Alias      MyLepD_s1_2536+   D'_s1+
Alias      MyD0              D0
Alias      Myanti-D0         anti-D0
Alias      MyD*-             D*-
Alias      MyD*+             D*+
Alias      MyD_s1_2536-      D'_s1-
Alias      MyD_s1_2536+      D'_s1+
Alias      MyB0              B0
Alias      Myanti-B0         anti-B0

ChargeConj MyLepTau+        MyLepTau-
ChargeConj MyLepD0          MyLepanti-D0
ChargeConj MyLepD+          MyLepD-
ChargeConj MyLepD*0         MyLepanti-D*0
ChargeConj MyLepD*+         MyLepD*-
ChargeConj MyLepD_s+        MyLepD_s-
ChargeConj MyLepD_s*+       MyLepD_s*-
ChargeConj MyLepD_s1+       MyLepD_s1-
ChargeConj MyLepD_s1_2536-  MyLepD_s1_2536+
ChargeConj MyD0             Myanti-D0
ChargeConj MyD*-            MyD*+
ChargeConj MyD_s1_2536-     MyD_s1_2536+
ChargeConj MyB0             Myanti-B0

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

Decay MyLepTau+
1.000      mu+  nu_mu   anti-nu_tau         TAULNUNU;
Enddecay
CDecay MyLepTau-

Decay MyLepD0
0.03410 K-      mu+     nu_mu                           PHOTOS  ISGW2;
0.01890 K*-     mu+     nu_mu                           PHOTOS  ISGW2;
0.00267 pi-     mu+     nu_mu                           PHOTOS  ISGW2;
0.00150 rho-    mu+     nu_mu                           PHOTOS  ISGW2;
0.00076 K_1-    mu+     nu_mu                           PHOTOS  ISGW2;
0.00077 anti-K0 pi-     mu+     nu_mu                   PHOTOS   PHSP;
0.00039 K-      pi0     mu+     nu_mu                   PHOTOS   PHSP;
0.00030 K_2*-   mu+     nu_mu                           PHOTOS  ISGW2; # copy from electron
Enddecay
CDecay MyLepanti-D0

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

Decay MyLepD*0
0.647 MyLepD0      pi0                                  VSS; #[Reconstructed PDG2011]
0.353 MyLepD0      gamma                                VSP_PWAVE; #[Reconstructed PDG2011]
Enddecay
CDecay MyLepanti-D*0

Decay MyLepD*+
# 0.677*60.8e-3 (Du -> muX) = 41.16e-3
0.4116    MyLepD0  pi+                        VSS;
# 0.3070 * 158.8e-3 = 48.75e-3
0.4875    MyLepD+  pi0                        VSS;
# 0.016 * 158.8e-3 = 2.54e-3
0.025     MyLepD+  gamma                      VSP_PWAVE;
Enddecay
# Tot = 92.45e-3
CDecay MyLepD*-

Decay MyLepD_s+
0.02390 phi     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.02320 eta     mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00800 eta'    mu+     nu_mu                           PHOTOS  ISGW2; #[Reconstructed PDG2011]
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

Decay MyLepD_s1+
0.48      MyLepD_s*+ pi0                 PARTWAVE 1.0 0.0 0.0 0.0 0.0 0.0;
0.18      MyLepD_s+  gamma               VSP_PWAVE;
0.04      MyLepD_s+  pi+ pi-             PHSP;
Enddecay
CDecay MyLepD_s1-

Decay MyLepD_s1_2536+
# 0.5 * 92.45e-3 (Dd* -> muX) = 46.23e-3
0.4623  MyLepD*+ K0 PHSP;
# 0.5 * 60.8e-3 (Du -> muX) = 30.4e-3
0.3040  MyLepD*0 K+ PHSP;
Enddecay
# Tot = 76.63
CDecay MyLepD_s1_2536-

Decay MyD_s1_2536+
1.000  MyD*+ K0 PHSP;
Enddecay
CDecay MyD_s1_2536-

Decay MyB0
# 9.3e-3 (Gamma 101) * 75.4e-3 (Ds -> muX) = 701.22e-6 = 0.7012e-3
0.7012   MyD*-        MyLepD_s1+                        SVV_HELAMP 0.4904 0. 0.7204 0. 0.4904 0.; #[Reconstructed PDG2011]
# 0.5*0.28e-3 (Gamma 103 / 2) * 159e-3 (Dd -> muX) = 22.26e-6 = 0.0223e-3
0.0223   MyLepD-      MyD_s1_2536+                      PHSP;
# 0.5*0.5e-3 (gamma 106/2) * 92.45e-3 (Dd* -> muX) = 23.11e-6 = 0.0231e-3
0.0231    MyLepD*-     MyD_s1_2536+                      PHSP;
# 0.5e-3 (Gamma 106) * 76.63e-3 (D_s1_2536 -> muX) = 38.32e-6 = 0.0383e-3
0.0383    MyD*-        MyLepD_s1_2536+                   PHSP;
Enddecay
# Tot = 78.49e-3
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

bmesonFilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(999999),
    MinEta = cms.untracked.double(-999999),
    MinPt = cms.untracked.double(0),
    ParticleID = cms.untracked.int32(511) # B0
)

tagfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13), ## mu
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


ProductionFilterSequence = cms.Sequence(generator + bmesonFilter + tagfilter + D0filter)
