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
Alias      MyLepD0         D0
Alias      MyLepanti-D0    anti-D0
Alias      MyLepD*0        D*0
Alias      MyLepanti-D*0   anti-D*0
Alias      MyD0            D0
Alias      Myanti-D0       anti-D0
Alias      MyD*-           D*-
Alias      MyD*+           D*+
Alias      MyD_s1_2536-    D_s2*- #Hijacking this other resonance even if has the wrong spin
Alias      MyD_s1_2536+    D_s2*+ #Hijacking this other resonance even if has the wrong spin
Alias      MyB+            B+
Alias      MyB-            B-

ChargeConj MyLepD0        MyLepanti-D0
ChargeConj MyLepD*0       MyLepanti-D*0
ChargeConj MyD0           Myanti-D0
ChargeConj MyD*-          MyD*+
ChargeConj MyD_s1_2536-   MyD_s1_2536+
ChargeConj MyB+           MyB-

Decay MyD0
1.000       K-  pi+           PHSP;
Enddecay
CDecay Myanti-D0

Decay MyD*-
1.000       Myanti-D0 pi-     VSS;
Enddecay
CDecay MyD*+

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

Decay MyLepD*0
0.647 MyLepD0      pi0                                  VSS; #[Reconstructed PDG2011]
0.353 MyLepD0      gamma                                VSP_PWAVE; #[Reconstructed PDG2011]
Enddecay
CDecay MyLepanti-D*0


Decay MyD_s1_2536+
1.000  MyD*+ K0 PHSP;
Enddecay
CDecay MyD_s1_2536-


Decay MyB+
0.01   MyLepanti-D0   MyD_s1_2536+         PHSP;
0.005  MyLepanti-D*0  MyD_s1_2536+         PHSP;
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
bmesonFilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(999999),
    MinEta = cms.untracked.double(-999999),
    MinPt = cms.untracked.double(0),
    ParticleID = cms.untracked.int32(521) # B+/-
)

tagfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13), ## mu
    MotherID = cms.untracked.int32(421) ## D0
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
