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
            operates_on_particles = cms.vint32(521, -511, 511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyD0   D0
Alias      Myanti-D0   anti-D0
ChargeConj MyD0   Myanti-D0
#
Decay MyD0
1.000      K-  pi+                PHSP;
Enddecay
CDecay Myanti-D0
#
Alias     MyD*-    D*-
Decay MyD*-
1.000      Myanti-D0 pi-          VSS;
Enddecay
#
#
############# Force excited states decay #############
#
Alias myanti-D_10 anti-D_10
Decay myanti-D_10
0.6667    MyD*- pi+                        VVS_PWAVE  0.0 0.0 0.0 0.0 1.0 0.0;
Enddecay
#
Alias myanti-D'_10 anti-D'_10
Decay myanti-D'_10
0.6667    MyD*- pi+                        VVS_PWAVE  1.0 0.0 0.0 0.0 0.0 0.0;
Enddecay
#
Alias myanti-D_2*0 anti-D_2*0
Decay myanti-D_2*0
0.2090    MyD*- pi+                        TVS_PWAVE  0.0 0.0 1.0 0.0 0.0 0.0;
Enddecay
#
#
#
Decay B+
# From decay table of EvtGen
# 0.0045   myanti-D_10   mu+  nu_mu       PHOTOS   ISGW2;
# 0.0040   myanti-D'_10   mu+  nu_mu      PHOTOS   ISGW2;
# 0.0010   myanti-D_2*0   mu+  nu_mu      PHOTOS   ISGW2; # 0.0033*0.209/0.6667
# From PDG, including D** -> D* decay
0.0030   myanti-D_10   mu+  nu_mu       PHOTOS   ISGW2;
0.0027   myanti-D'_10   mu+  nu_mu      PHOTOS   ISGW2;
0.0010   myanti-D_2*0   mu+  nu_mu      PHOTOS   ISGW2;
Enddecay
#
#
# Probe side
#
Decay anti-B0
1.000     D*+ mu- anti-nu_mu         PHOTOS  ISGW2;
Enddecay
#
#
Decay B0
1.000     D*- mu+ nu_mu         PHOTOS  ISGW2;
Enddecay
#
End
"""
                                            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring('HardQCD:hardbbbar = on'),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########
tagfilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(511),  ## B0/anti-B0
    ChargeConjugation  = cms.untracked.bool(True),
    NumberDaughters    = cms.untracked.int32(3),
    DaughterIDs        = cms.untracked.vint32(-413, -13, 14),
    MinPt              = cms.untracked.vdouble(-1., 6.8, -1.),
    MinEta             = cms.untracked.vdouble(-9999999., -1.55, -9999999.),
    MaxEta             = cms.untracked.vdouble( 9999999.,  1.55, 9999999.)
)


mufilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(2.3),
    MinEta = cms.untracked.double(-2.3),
    MinPt = cms.untracked.double(3.),
    ParticleID = cms.untracked.int32(13),
    MotherID = cms.untracked.int32(521)
)


ProductionFilterSequence = cms.Sequence(generator + tagfilter + mufilter)
